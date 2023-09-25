# ウェブからの関連リソース

人々はGPTからの出力を改善するための素晴らしいツールや論文を書いています。以下は私たちが見た中で面白いものです。

## プロンプトライブラリとツール

- [Guidance](https://github.com/microsoft/guidance): Microsoftの便利なPythonライブラリで、Handlebarsテンプレートを使用して生成、プロンプティング、論理制御を交互に行います。
- [LangChain](https://github.com/hwchase17/langchain): 言語モデルプロンプトのシーケンスを連鎖させるための人気のあるPython/JavaScriptライブラリ。
- [FLAML（高速自動機械学習および調整のためのライブラリ）](https://microsoft.github.io/FLAML/docs/Getting-Started/): モデル、ハイパーパラメータ、およびその他の調整可能な選択肢の自動化に役立つPythonライブラリ。
- [Chainlit](https://docs.chainlit.io/overview): チャットボットインターフェースを作成するためのPythonライブラリ。
- [Guardrails.ai](https://shreyar.github.io/guardrails/): 出力の検証と失敗の再試行を行うためのPythonライブラリ。まだアルファ版なので、鋭いエッジとバグがある可能性があります。
- [Semantic Kernel](https://github.com/microsoft/semantic-kernel): MicrosoftのPython/C#/Javaライブラリで、プロンプトのテンプレート化、関数連鎖、ベクトル化されたメモリ、インテリジェントなプランニングをサポートします。
- [Prompttools](https://github.com/hegelai/prompttools): モデル、ベクトルDB、およびプロンプトのテストと評価に使用できるオープンソースのPythonツール。
- [Outlines](https://github.com/normal-computing/outlines): プロンプティングを単純化し、生成を制約するためのPythonライブラリ。
- [Promptify](https://github.com/promptslab/Promptify): 言語モデルを使用してNLPタスクを実行するための小さなPythonライブラリ。
- [Scale Spellbook](https://scale.com/spellbook): 言語モデルアプリを構築し、比較し、配信するための有料製品。
- [PromptPerfect](https://promptperfect.jina.ai/prompts): プロンプトのテストと改善に使用する有料製品。
- [Weights & Biases](https://wandb.ai/site/solutions/llmops): モデルトレーニングとプロンプトエンジニアリングの実験を追跡するための有料製品。
- [OpenAI Evals](https://github.com/openai/evals): 言語モデルとプロンプトのタスクパフォーマンスを評価するためのオープンソースライブラリ。
- [LlamaIndex](https://github.com/jerryjliu/llama_index): LLMアプリケーションにデータを追加するためのPythonライブラリ。
- [Arthur Shield](https://www.arthur.ai/get-started): 有害性、幻覚、プロンプトの注入などを検出するための有料製品。
- [LMQL](https://lmql.ai): LLMの相互作用のためのプログラミング言語で、型付きプロンプティング、制御フロー、制約、ツールをサポートしています。

## プロンプトガイド

- [Brexのプロンプトエンジニアリングガイド](https://github.com/brexhq/prompt-engineering): Brexの言語モデルとプロンプトエンジニアリングの紹介。
- [promptingguide.ai](https://www.promptingguide.ai/): 多くのテクニックを示すプロンプトエンジニアリングガイド。
- [OpenAI Cookbook: 信頼性を向上させるためのテクニック](https://github.com/openai/openai-cookbook/blob/main/techniques_to_improve_reliability.md): 言語モデルのプロンプトに関するテクニックの若干古い（2022年9月）レビュー。
- [Lil'Logのプロンプトエンジニアリング](https://lilianweng.github.io/posts/2023-03-15-prompt-engineering/): OpenAIの研究者によるプロンプトエンジニアリング文献のレビュー（2023年3月現在）。
- [learnprompting.org](https://learnprompting.org/): プロンプトエンジニアリングの導入コース。

## ビデオコース

- [Andrew NgのDeepLearning.AI](https://www.deeplearning.ai/short-courses/chatgpt-prompt-engineering-for-developers/): 開発者向けのプロンプトエンジニアリングに関する短期コース。
- [Andrej KarpathyによるGPTの構築](https://www.youtube.com/watch?v=kCc8FmEb1nY): GPTの基礎となる機械学習の詳細な解説。
- [DAIR.AI

によるプロンプトエンジニアリング](https://www.youtube.com/watch?v=dOxUroR57xs): 各種プロンプトエンジニアリングテクニックに関する1時間のビデオ。

## 推論力向上のための高度なプロンプティングに関する論文

- [Chain-of-Thoughtプロンプティングが大規模言語モデルの推論力を引き出す（2022年）](https://arxiv.org/abs/2201.11903): 少数のショットプロンプトを使用してモデルにステップバイステップで考えさせることは推論力を向上させます。 PaLMの数学の単語問題（GSM8K）のスコアは18％から57％に上昇します。
- [自己整合性が大規模言語モデルの思考連鎖推論を改善する（2022年）](https://arxiv.org/abs/2203.11171): 複数の出力からの投票はさらに精度を向上させます。 40の出力を跨いで投票することで、PaLMの数学の単語問題のスコアはさらに向上し、57％から74％に、および`code-davinci-002`のスコアは60％から78％に上昇します。
- [思考のツリー：大規模言語モデルを使用した慎重な問題解決（2023年）](https://arxiv.org/abs/2305.10601): ステップバイステップの推論のツリーを検索することが、思考連鎖の投票よりもさらに助けになります。これにより、`GPT-4`のクリエイティブライティングとクロスワードのスコアが向上します。
- [言語モデルはゼロショットの推論者である（2022年）](https://arxiv.org/abs/2205.11916): 命令従属モデルにステップバイステップで考えさせることは推論力を向上させます。 `text-davinci-002`の数学の単語問題（GSM8K）のスコアは13％から41％に上昇します。
- [大規模言語モデルは人間レベルのプロンプトエンジニアです（2023年）](https://arxiv.org/abs/2211.01910): 可能なプロンプトを自動的に検索することで、数学の単語問題（GSM8K）のスコアを43％に引き上げ、言語モデルはゼロショットの推論者で書かれた人間のプロンプトを2ポイント上回ります。
- [Reprompting：Gibbsサンプリングを介した自動思考連鎖プロンプトの推論（2023年）](https://arxiv.org/abs/2305.09993): 可能な思考連鎖プロンプトを自動的に検索することで、ChatGPTのいくつかのベンチマークで0〜20ポイントの改善が見られます。
- [大規模言語モデルを使用した信頼性ある推論（2022年）](https://arxiv.org/abs/2208.14271): 代替選択および推論プロンプトによって生成された思考連鎖、選択-推論ループを停止するときを選択するハルターモデル、複数の推論パスを検索するための値関数、幻覚を回避するための文ラベルを組み合わせるシステムによって推論力を向上させます。
- [STaR：推論を推論することで思考連鎖をブートストラップ（2022年）](https://arxiv.org/abs/2203.14465): 思考連鎖推論は微調整を介してモデルに組み込むことができます。回答キーがあるタスクの場合、言語モデルによって例の思考連鎖を生成できます。
- [ReAct：言語モデルでの推論と行動の協力（2023年）](https://arxiv.org/abs/2210.03629): ツールや環境があるタスクの場合、思考ステップ（何をするかを考える）とアクション（ツールや環境から情報を取得する）を予定通りに交互に切り替えることで、思考連鎖がより効果的に機能します。
- [Reflexion：事前の失敗のメモリを持つ自律エージェント（2023年）](https://arxiv.org/abs/2303.11366): 前回の失敗のメモリを持ってタスクを再試行することで、後続のパフォーマンスが向上します。
- [Demonstrate-Search-Predict：知識密度の高いNLPのための検索と言語モデルを組み合わ

せる（2023年）](https://arxiv.org/abs/2212.14024): 知識を備えたモデルは、 "検索してから読む"を使用して改善でき、マルチホップの検索チェーンを使用してさらに改善できます。
- [大規模な言語モデルによるファクトゥアル性と推論の向上（2023年）](https://arxiv.org/abs/2305.14325): ChatGPTエージェント間でのディベートを生成することで、さまざまなベンチマークのスコアが向上します。数学の単語問題のスコアは77％から85％に上昇します。