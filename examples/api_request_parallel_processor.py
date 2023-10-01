"""
APIリクエスト並列処理スクリプト

このスクリプトはOpenAI APIに対するリクエストを並列に処理しながら、レート制限を超えないように調整します。

特長:
- メモリを節約するためにファイルからリクエストをストリーミング
- 最大のスループットを実現するためにリクエストを並列に実行
- レート制限を超えないようにリクエストとトークンの使用量を調整
- データの欠落を防ぐために失敗したリクエストを{max_attempts}回までリトライ
- リクエストの問題を診断するためのエラーロギング

例のコマンド:
```
python examples/api_request_parallel_processor.py \
  --requests_filepath examples/data/example_requests_to_parallel_process.jsonl \
  --save_filepath examples/data/example_requests_to_parallel_process_results.jsonl \
  --request_url https://api.openai.com/v1/embeddings \
  --max_requests_per_minute 1500 \
  --max_tokens_per_minute 6250000 \
  --token_encoding_name cl100k_base \
  --max_attempts 5 \
  --logging_level 20
```

引数:
- requests_filepath : str
    - 処理するリクエストを含むファイルへのパス
    - jsonl形式のファイルで、各行がAPIパラメータとオプションのメタデータフィールドを持つjsonオブジェクトである必要があります
- その他の引数は原文のdocstringを参照

このスクリプトは以下のように構成されています:
    - インポート
    - main()の定義
    - データクラスの定義
    - 関数の定義
    - main()の実行
"""


# 既存のコードに変更はありません。


# imports
import argparse  # for running script from command line
import asyncio  # for running API calls concurrently
import json  # for saving results to a jsonl file
import logging  # for logging rate limit warnings and other messages
import os  # for reading API key
import re  # for matching endpoint from request URL
from dataclasses import dataclass, field  # for storing API inputs, outputs, and metadata
from typing import List, Union  # for type hinting
import time  # for sleeping after rate limit is hit

import aiohttp  # for making API calls concurrently
import tiktoken  # for counting tokens


async def process_api_requests_from_file(
    requests_filepath: str,
    save_filepath: str,
    request_url: str,
    api_key: str,
    max_requests_per_minute: float,
    max_tokens_per_minute: float,
    token_encoding_name: str,
    max_attempts: int,
    logging_level: int,
):
    """
    APIリクエストを並列に処理し、レート制限を超えないように調整します。

    Args:
        requests_filepath (str): 処理するリクエストを含むファイルへのパス。
        save_filepath (str): 結果を保存するファイルへのパス。
        request_url (str): APIエンドポイントのURL。
        api_key (str): 使用するAPIキー。
        max_requests_per_minute (float): 分あたりの最大リクエスト数。
        max_tokens_per_minute (float): 分あたりの最大トークン数。
        token_encoding_name (str): 使用するトークンエンコーディングの名前。
        max_attempts (int): 失敗したリクエストを再試行する回数。
        logging_level (int): 使用するロギングレベル。
    """
    # constants
    seconds_to_pause_after_rate_limit_error = 15
    seconds_to_sleep_each_loop = 0.001  # 1 ms limits max throughput to 1,000 requests per second

    # initialize logging
    logging.basicConfig(level=logging_level)
    logging.debug(f"Logging initialized at level {logging_level}")

    # infer API endpoint and construct request header
    api_endpoint = api_endpoint_from_url(request_url)
    request_header = {"Authorization": f"Bearer {api_key}"}

    # initialize trackers
    queue_of_requests_to_retry = asyncio.Queue()
    task_id_generator = task_id_generator_function()  # generates integer IDs of 1, 2, 3, ...
    status_tracker = StatusTracker()  # single instance to track a collection of variables
    next_request = None  # variable to hold the next request to call

    # initialize available capacity counts
    available_request_capacity = max_requests_per_minute
    available_token_capacity = max_tokens_per_minute
    last_update_time = time.time()

    # initialize flags
    file_not_finished = True  # after file is empty, we'll skip reading it
    logging.debug("Initialization complete.")

    # initialize file reading
    with open(requests_filepath) as file:
        # `requests` will provide requests one at a time
        requests = file.__iter__()
        logging.debug("File opened. Entering main loop")

        while True:
            # get next request (if one is not already waiting for capacity)
            if next_request is None:
                if not queue_of_requests_to_retry.empty():
                    next_request = queue_of_requests_to_retry.get_nowait()
                    logging.debug(f"Retrying request {next_request.task_id}: {next_request}")
                elif file_not_finished:
                    try:
                        # get new request
                        request_json = json.loads(next(requests))
                        next_request = APIRequest(
                            task_id=next(task_id_generator),
                            request_json=request_json,
                            token_consumption=num_tokens_consumed_from_request(
                                request_json, api_endpoint, token_encoding_name
                            ),
                            attempts_left=max_attempts,
                            metadata=request_json.pop("metadata", None),
                        )
                        status_tracker.num_tasks_started += 1
                        status_tracker.num_tasks_in_progress += 1
                        logging.debug(f"Reading request {next_request.task_id}: {next_request}")
                    except StopIteration:
                        # if file runs out, set flag to stop reading it
                        logging.debug("Read file exhausted")
                        file_not_finished = False

            # update available capacity
            current_time = time.time()
            seconds_since_update = current_time - last_update_time
            available_request_capacity = min(
                available_request_capacity + max_requests_per_minute * seconds_since_update / 60.0,
                max_requests_per_minute,
            )
            available_token_capacity = min(
                available_token_capacity + max_tokens_per_minute * seconds_since_update / 60.0,
                max_tokens_per_minute,
            )
            last_update_time = current_time

            # if enough capacity available, call API
            if next_request:
                next_request_tokens = next_request.token_consumption
                if available_request_capacity >= 1 and available_token_capacity >= next_request_tokens:
                    # update counters
                    available_request_capacity -= 1
                    available_token_capacity -= next_request_tokens
                    next_request.attempts_left -= 1

                    # call API
                    asyncio.create_task(
                        next_request.call_api(
                            request_url=request_url,
                            request_header=request_header,
                            retry_queue=queue_of_requests_to_retry,
                            save_filepath=save_filepath,
                            status_tracker=status_tracker,
                        )
                    )
                    next_request = None  # reset next_request to empty

            # if all tasks are finished, break
            if status_tracker.num_tasks_in_progress == 0:
                break

            # main loop sleeps briefly so concurrent tasks can run
            await asyncio.sleep(seconds_to_sleep_each_loop)

            # if a rate limit error was hit recently, pause to cool down
            seconds_since_rate_limit_error = time.time() - status_tracker.time_of_last_rate_limit_error
            if seconds_since_rate_limit_error < seconds_to_pause_after_rate_limit_error:
                remaining_seconds_to_pause = seconds_to_pause_after_rate_limit_error - seconds_since_rate_limit_error
                await asyncio.sleep(remaining_seconds_to_pause)
                # ^e.g., if pause is 15 seconds and final limit was hit 5 seconds ago
                logging.warn(
                    f"Pausing to cool down until {time.ctime(status_tracker.time_of_last_rate_limit_error + seconds_to_pause_after_rate_limit_error)}"
                )

        # after finishing, log final status
        logging.info(f"""Parallel processing complete. Results saved to {save_filepath}""")
        if status_tracker.num_tasks_failed > 0:
            logging.warning(
                f"{status_tracker.num_tasks_failed} / {status_tracker.num_tasks_started} requests failed. Errors logged to {save_filepath}."
            )
        if status_tracker.num_rate_limit_errors > 0:
            logging.warning(
                f"{status_tracker.num_rate_limit_errors} rate limit errors received. Consider running at a lower rate."
            )


# dataclasses


@dataclass
class StatusTracker:
    """
    スクリプトの進行状況に関するメタデータを格納します。
    インスタンスは1つだけ生成されます。
    """

    num_tasks_started: int = 0
    num_tasks_in_progress: int = 0  # script ends when this reaches 0
    num_tasks_succeeded: int = 0
    num_tasks_failed: int = 0
    num_rate_limit_errors: int = 0
    num_api_errors: int = 0  # excluding rate limit errors, counted above
    num_other_errors: int = 0
    time_of_last_rate_limit_error: int = 0  # used to cool off after hitting rate limits


@dataclass
class APIRequest:
    """
    APIリクエストの入力、出力、その他のメタデータを格納します。
    API呼び出しを行うメソッドも含まれています。
    """

    task_id: int
    request_json: dict
    token_consumption: int
    attempts_left: int
    metadata: dict
    result: list = field(default_factory=list)

    async def call_api(
        self,
        request_url: str,
        request_header: dict,
        retry_queue: asyncio.Queue,
        save_filepath: str,
        status_tracker: StatusTracker,
    ):
        """Calls the OpenAI API and saves results."""
        logging.info(f"Starting request #{self.task_id}")
        error = None
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(url=request_url, headers=request_header, json=self.request_json) as response:
                    response = await response.json()
            if "error" in response:
                logging.warning(f"Request {self.task_id} failed with error {response['error']}")
                status_tracker.num_api_errors += 1
                error = response
                if "Rate limit" in response["error"].get("message", ""):
                    status_tracker.time_of_last_rate_limit_error = time.time()
                    status_tracker.num_rate_limit_errors += 1
                    status_tracker.num_api_errors -= 1  # rate limit errors are counted separately

        except Exception as e:  # catching naked exceptions is bad practice, but in this case we'll log & save them
            logging.warning(f"Request {self.task_id} failed with Exception {e}")
            status_tracker.num_other_errors += 1
            error = e
        if error:
            self.result.append(error)
            if self.attempts_left:
                retry_queue.put_nowait(self)
            else:
                logging.error(f"Request {self.request_json} failed after all attempts. Saving errors: {self.result}")
                data = (
                    [self.request_json, [str(e) for e in self.result], self.metadata]
                    if self.metadata
                    else [self.request_json, [str(e) for e in self.result]]
                )
                append_to_jsonl(data, save_filepath)
                status_tracker.num_tasks_in_progress -= 1
                status_tracker.num_tasks_failed += 1
        else:
            data = [self.request_json, response, self.metadata] if self.metadata else [self.request_json, response]
            append_to_jsonl(data, save_filepath)
            status_tracker.num_tasks_in_progress -= 1
            status_tracker.num_tasks_succeeded += 1
            logging.debug(f"Request {self.task_id} saved to {save_filepath}")


# functions


def api_endpoint_from_url(request_url):
    """
    リクエストURLからAPIエンドポイントを抽出します。

    Parameters:
    -----------
    request_url: APIエンドポイントのURL

    Returns:
    --------
    APIエンドポイント名を返します。
    """
    match = re.search("^https://[^/]+/v\\d+/(.+)$", request_url)
    return match[1]


def append_to_jsonl(data: dict, filename: str) -> None:
    """
    jsonのペイロードをjsonlファイルの末尾に追加します。

    Parameters:
    - data: dict -- 書き込むデータ
    - filename: str -- jsonlファイル名
    """
    json_string = json.dumps(data)
    with open(filename, "a") as f:
        f.write(f"{json_string}\n")


def count_tokens(input_data: Union[str, List[str]], encoding) -> int:
    """
    与えられた入力データのトークン数をカウントします。

    Parameters:
    - input_data: Union[str, List[str]] -- カウントするテキスト
    - encoding -- トークンエンコーディング

    Returns:
    int -- トークン数
    """
    if isinstance(input_data, str):
        return len(encoding.encode(input_data))
    elif isinstance(input_data, list):
        return sum([len(encoding.encode(i)) for i in input_data])
    else:
        raise TypeError("入力データは文字列または文字列のリストでなければなりません。")


def num_tokens_consumed_from_request(
    request_json: dict,
    api_endpoint: str,
    token_encoding_name: str,
) -> int:
    """
    リクエストから消費されるトークン数をカウントします。completionとembeddingリクエストのみをサポートしています。

    Parameters:
    - request_json: dict -- リクエストのjsonデータ
    - api_endpoint: str -- APIエンドポイント
    - token_encoding_name: str -- トークンエンコーディング名

    Returns:
    int -- 消費されるトークン数
    """
    Tokenizer = tiktoken.Tokenizer()
    encoding = Tokenizer.get_encoding(token_encoding_name)

    if api_endpoint.endswith("completions"):
        max_tokens = request_json.get("max_tokens", 15)
        n = request_json.get("n", 1)
        completion_tokens = n * max_tokens

        if api_endpoint.startswith("chat/"):
            num_tokens = sum(
                [
                    4 + sum(len(encoding.encode(value)) for key, value in message.items())
                    for message in request_json["messages"]
                ]
            )
            num_tokens += 2
            return num_tokens + completion_tokens
        else:
            prompt = request_json["prompt"]
            return count_tokens(prompt, encoding) + completion_tokens

    elif api_endpoint == "embeddings":
        input_data = request_json["input"]
        return count_tokens(input_data, encoding)

    else:
        raise NotImplementedError(f'APIエンドポイント "{api_endpoint}" はこのスクリプトで実装されていません。')


def task_id_generator_function() -> int:
    """
    0, 1, 2, などの整数を生成します。
    """
    task_id = 0
    while True:
        yield task_id
        task_id += 1


# run script


if __name__ == "__main__":
    # parse command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("--requests_filepath")
    parser.add_argument("--save_filepath", default=None)
    parser.add_argument("--request_url", default="https://api.openai.com/v1/embeddings")
    parser.add_argument("--api_key", default=os.getenv("OPENAI_API_KEY"))
    parser.add_argument("--max_requests_per_minute", type=int, default=3_000 * 0.5)
    parser.add_argument("--max_tokens_per_minute", type=int, default=250_000 * 0.5)
    parser.add_argument("--token_encoding_name", default="cl100k_base")
    parser.add_argument("--max_attempts", type=int, default=5)
    parser.add_argument("--logging_level", default=logging.INFO)
    args = parser.parse_args()

    if args.save_filepath is None:
        args.save_filepath = args.requests_filepath.replace(".jsonl", "_results.jsonl")

    # run script
    asyncio.run(
        process_api_requests_from_file(
            requests_filepath=args.requests_filepath,
            save_filepath=args.save_filepath,
            request_url=args.request_url,
            api_key=args.api_key,
            max_requests_per_minute=float(args.max_requests_per_minute),
            max_tokens_per_minute=float(args.max_tokens_per_minute),
            token_encoding_name=args.token_encoding_name,
            max_attempts=int(args.max_attempts),
            logging_level=int(args.logging_level),
        )
    )


"""

付録
openai-cookbook/examples/data/example_requests_to_parallel_process.jsonl という例のリクエストファイルには、text-embedding-ada-002 モデルへの10,000件のリクエストが含まれています。

このファイルは以下のコードで生成されました。

```python
import json

filename = "data/example_requests_to_parallel_process.jsonl"
n_requests = 10_000
jobs = [{"model": "text-embedding-ada-002", "input": str(x) + "\n"} for x in range(n_requests)]
with open(filename, "w") as f:
    for job in jobs:
        json_string = json.dumps(job)
        f.write(json_string + "\n")
```

すべてのJSONLファイルに共通して、コンテンツ内の改行が適切にエスケープされる必要があります（json.dumps はこれを自動的に行います）。


"""
