# 大規模言語モデルの使用方法

## 大規模言語モデルの動作原理

[大規模言語モデル][Large language models Blog Post]は、テキストをテキストにマップする関数です。入力テキスト文字列が与えられると、大規模言語モデルは次に続くテキストを予測します。

大規模言語モデルの魔法は、これらの予測の誤差を大量のテキストにわたって最小化するように訓練されることによって、モデルがこれらの予測に役立つ概念を学習することです。たとえば、以下のようなことを学習します：

* スペルの方法
* 文法の動作方法
* 言い換える方法
* 質問に答える方法
* 会話を続ける方法
* 多くの言語で書く方法
* コードを書く方法
* など

これらの能力は明示的にプログラムされたものではなく、訓練の結果としてすべて出現します。

GPT-3は[数百のソフトウェア製品][GPT3 Apps Blog Post]を動かしており、生産性向上のアプリ、教育アプリ、ゲームなどに利用されています。

## 大規模言語モデルの制御方法

大規模言語モデルへの入力の中でも、最も影響力のあるものはテキストプロンプトです。

大規模言語モデルには、いくつかの方法で出力を生成させることができます：

* **指示**: モデルに何を望むかを伝える
* **完了**: モデルに望む内容の開始部分を完成させる
* **デモンストレーション**: モデルに望む内容を示す。具体的には以下の方法で行えます：
  * プロンプト内のいくつかの例
  * ファインチューニングトレーニングデータセット内の数百または数千の例

それぞれの例を以下に示します。

### 指示型プロンプト

指示に従うモデル（たとえば、`text-davinci-003`または`text-`で始まる任意のモデル）は、指示に従うように特別に設計されています。指示をプロンプトの一番上に書いて（または一番下に、または両方に）、モデルは指示に従うよう最善を尽くし、その後停止します。指示は詳細であっても構いませんので、望む出力を詳細に説明する段落を書くのをためらわないでください。

指示型プロンプトの例：

```text
以下の引用から著者の名前を抜き出してください。

“Some humans theorize that intelligent species go extinct before they can expand into outer space. If they're correct, then the hush of the night sky is the silence of the graveyard.”
― Ted Chiang, Exhalation
```

出力：

```text
Ted Chiang
```

### 完了型プロンプトの例

完了型プロンプトは、大規模言語モデルが次に続くと思われるテキストを書こうとする方法を利用します。モデルを誘導するために、望む出力が完成するようなパターンや文を開始してみてください。直接の指示と比較して、大規模言語モデルを誘導するためにはさらに注意と実験が必要かもしれません。また、モデルは必ずしも停止する方法を知らないため、望ましい出力を超えて生成されるテキストを切り捨てるために停止シーケンスや後処理が必要です。

完了型プロンプトの例：

```text
“Some humans theorize that intelligent species go extinct before they can expand into outer space. If they're correct, then the hush of the night sky is the silence of the graveyard.”
― Ted Chiang, Exhalation

この引用の著者は
```

出力：

```text
 Ted Chiang
```

### デモンストレーション型プロンプトの例（フューショット学習）

完了型プロンプトと同様に、デモンストレーションはモデルに望む動作を示すことができます。このアプローチは、プロンプト内で提供された少数の例からモデルが学習するため、フューショット学習と呼ばれることもあります。

デモンストレーション型プロンプトの例：

```text
引用：
“When the reasoning mind is forced to confront the impossible again and again, it has no choice but to adapt.”
― N.K. Jemisin, The Fifth Season
著者：N.K. Jemisin

引用：
“Some humans theorize that intelligent species go extinct before they can expand into outer space. If they're correct, then the hush of the night sky is the silence of the graveyard.”
― Ted Chiang, Exhalation
著者：
```

出力：

```text
 Ted Chiang
```

###

 ファインチューニング型プロンプトの例

十分な訓練例を用意すると、カスタムモデルを[ファインチューニング][Fine Tuning Docs]できます。この場合、指示は不要で、モデルは提供されたトレーニングデータからタスクを学習できます。ただし、プロンプトが終了し、出力が始まることをモデルに伝えるセパレータシーケンス（例：`->`または`###`または入力で一般的に現れない任意の文字列）を含めることが役立つ場合があります。セパレータシーケンスがない場合、モデルは望む回答を始める代わりに入力テキストを詳細に説明し続ける危険性があります。

ファインチューニング型プロンプトの例（同様のプロンプト完成ペアにカスタムトレーニングされたモデル用）：

```text
“Some humans theorize that intelligent species go extinct before they can expand into outer space. If they're correct, then the hush of the night sky is the silence of the graveyard.”
― Ted Chiang, Exhalation

###


```

出力：

```text
 Ted Chiang
```

## コードの能力

大規模言語モデルはテキストだけでなく、コードにも優れています。OpenAIの専用のコードモデルは[Codex]と呼ばれています。

Codexは[70以上の製品][Codex Apps Blog Post]を動かしており、以下のようなものが含まれています：

* [GitHub Copilot]（VS Codeおよび他のIDEでコードを自動補完）
* [Pygma](https://pygma.app/)（Figmaデザインをコードに変換）
* [Replit](https://replit.com/)（'Explain code'ボタンなどがあります）
* [Warp](https://www.warp.dev/)（AIコマンド検索を備えたスマートターミナル）
* [Machinet](https://machinet.net/)（Javaユニットテストテンプレートを生成）

注意：指示に従うテキストモデル（たとえば`text-davinci-002`）とは異なり、Codexは指示に従うように訓練されていません。その結果、適切なプロンプトの設計にはさらに注意が必要です。

### 追加のプロンプトのアドバイス

さらなるプロンプトの例については、[OpenAI Examples][OpenAI Examples]を参照してください。

一般的に、入力プロンプトはモデルの出力を改善するための最良のレバーです。以下のようなトリックを試すことができます：

* **より明示的な指示を与える。** たとえば、出力がカンマ区切りのリストであることを希望する場合、カンマ区切りのリストを返すように指示してください。答えがわからない場合には「答えがわからない」と言うように指示してください。
* **より良い例を提供する。** プロンプトで例を示す場合、例が多様で高品質であることを確認してください。
* **モデルに専門家のように回答するよう指示する。** モデルに高品質な出力または専門家が書いたかのような出力を生成するよう明示的に要求することで、モデルが専門家が書くと思うような高品質な回答を生成する可能性が高まります。たとえば、「以下の回答は正確で高品質で、専門家によって書かれたものです。」と言うように指示します。
* **モデルに推論の理由を説明するステップのシリーズを書くよう指示する。** たとえば、最終的な回答の前に「[ステップごとに考えてみましょう](https://arxiv.org/pdf/2205.11916v1.pdf)」のようなものを追加することで、最終的な回答が一貫性があり正確である可能性が高まります。



[Fine Tuning Docs]: https://beta.openai.com/docs/guides/fine-tuning
[Codex Apps Blog Post]: https://openai.com/blog/codex-apps/
[Large language models Blog Post]: https://openai.com/blog/better-language-models/
[GitHub Copilot]: https://copilot.github.com/
[Codex]: https://openai.com/blog/openai-codex/
[GPT3 Apps Blog Post]: https://openai.com/blog/gpt-3-apps/
[OpenAI Examples]: https://beta.openai.com/examples
