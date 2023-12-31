# ChatGPTとあなたのデータを活用して製品を強化する

Chatbot Kickstarterは、ChatGPT APIとあなた自身の知識ベースを使用して基本的なチャットボットを構築する手始めのリポジトリです。あなたが経由するフローは、元々[このスライド](https://drive.google.com/file/d/1dB-RQhZC_Q1iAsHkNNdkqtxxXqYODFYy/view?usp=share_link)で紹介されました。これは参照に役立つかもしれません。

このリポジトリには1つのノートブックと2つの基本的なStreamlitアプリが含まれています。
- `powering_your_products_with_chatgpt_and_your_data.ipynb`：データのトークン化、チャンク化、ベクトルデータベースへの埋め込み、およびその上にシンプルなQ&AおよびChatbot機能を構築するステップバイステップのプロセスを含むノートブック。
- `search.py`：検索ベースの知識ベースへの簡単なQ&Aを提供するStreamlitアプリ。
- `chat.py`：検索ベースの知識ベースをクエリするためのシンプルなChatbotを提供するStreamlitアプリ。

いずれかのバージョンのアプリを実行するには、各サブディレクトリのREADME.mdファイルの指示に従ってください。

## 仕組み

ノートブックは始めるのに最適な場所で、大まかに以下のようにレイアウトされています：
- **基盤を築く：**
    - ベクトルデータベースをベクトルとデータを受け入れるように設定する
    - データセットをロードし、データを埋め込み用にチャンク化し、ベクトルデータベースに格納する
- **製品にする：**
    - ユーザーがクエリを提供し、最も関連性の高いエントリを返す検索ステップを追加する
    - GPT-3を使用して検索結果を要約する
    - この基本的なQ&AアプリをStreamlitで試す
- **堀を築く：**
    - コンテキストを管理し、ボットと対話するためのAssistantクラスを作成する
    - セマンティックサーチコンテキストを使用して質問に答えるためにChatbotを使用する
    - この基本的なChatbotアプリをStreamlitで試す

ノートブックを実行し、2つのStreamlitアプリを試したら、有用なスニペットを抜き出し、独自のQ&AまたはChatアプリを開始する準備が整います。

## 制限事項

- このアプリはベクトルデータベースとしてRedisを使用していますが、必要に応じて`../examples/vector_databases`で強調されている他の多くのオプションがあります。
- これは単純なスタートポイントです。ユースケースを展開する際に問題が発生した場合、次のような調整が必要かもしれません（非網羅的なリスト）：
    - モデルのためのプロンプトとパラメータを正確に回答するために調整する
    - より関連性の高い結果を返すために検索を調整する
    - 検索結果を最も効果的に取得するためのチャンク化/埋め込みアプローチを調整する