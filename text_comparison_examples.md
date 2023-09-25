# テキスト比較の例

[OpenAI APIの埋め込みエンドポイント](https://beta.openai.com/docs/guides/embeddings)は、テキストの要素間の関連性や類似性を測定するために使用できます。

GPT-3のテキスト理解能力を活用して、この埋め込みは教師なし学習と転移学習の設定において[最先端の結果を達成](https://arxiv.org/abs/2201.10005)しました。

埋め込みは、セマンティック検索、推薦、クラスタ分析、ほぼ重複の検出などに使用できます。

詳細については、OpenAIのブログ投稿を参照してください：

* [テキストとコードの埋め込みの紹介（2022年1月）](https://openai.com/blog/introducing-text-and-code-embeddings/)
* [新しく改良された埋め込みモデル（2022年12月）](https://openai.com/blog/new-and-improved-embedding-model/)

他の埋め込みモデルとの比較には、[Massive Text Embedding Benchmark（MTEB）リーダーボード](https://huggingface.co/spaces/mteb/leaderboard)を参照してください。

## セマンティック検索

埋め込みは、単独で、またはより大きなシステムの一機能として検索に使用できます。

検索のための埋め込みの最もシンプルな使い方は以下の通りです：

* 検索前（事前計算）：
  * テキストコーパスをトークン制限（`text-embedding-ada-002`の場合は8,191トークン）より小さいチャンクに分割します。
  * 各テキストチャンクを埋め込みます。
  * これらの埋め込みを自分自身のデータベース、またはベクトル検索プロバイダー（例：[Pinecone](https://www.pinecone.io)、[Weaviate](https://weaviate.io)、[Qdrant](https://qdrant.tech)）に保存します。
* 検索時（ライブ計算）：
  * 検索クエリを埋め込みます。
  * データベース内で最も近い埋め込みを見つけます。
  * トップの結果を返します。

検索のための埋め込みの使用例は、[Semantic_text_search_using_embeddings.ipynb](examples/Semantic_text_search_using_embeddings.ipynb)で示されています。

より高度な検索システムでは、埋め込みのコサイン類似度を、検索結果のランキングにおける多くの特徴のうちの一つとして使用できます。

## 質問応答

GPT-3から確実に正確な回答を得る最良の方法は、正確な答えを見つけることができるソースドキュメントを提供することです。上記のセマンティック検索の手法を使用して、ドキュメントのコーパスから関連する情報を効率よく検索し、その情報をGPT-3にプロンプトで提供して質問に答えることができます。これについては、[Question_answering_using_embeddings.ipynb](examples/Question_answering_using_embeddings.ipynb)で示しています。

## 推薦

推薦は検索に非常に似ていますが、フリーフォームのテキストクエリの代わりに、入力はセット内のアイテムです。

埋め込みを推薦に使用する方法の例は、[Recommendation_using_embeddings.ipynb](examples/Recommendation_using_embeddings.ipynb)で示されています。

検索と同様に、これらのコサイン類似度スコアは、単独でアイテムをランク付けするために使用することも、より大きなランキングアルゴリズム内の特徴として使用することもできます。

## 埋め込みのカスタマイズ

OpenAIの埋め込みモデルの重みは微調整できませんが、それでもトレーニングデータを使用してアプリケーションに合わせて埋め込みをカスタマイズすることができます。

[Customizing_embeddings.ipynb](examples/Customizing_embeddings.ipynb)では、トレーニングデータを使用して埋め込みをカスタマイズする方法の一例を提供しています。この方法のアイデアは、新しいカスタマイズされた埋め込みを取得するために埋め込みベクトルに掛け算するカスタム行列を訓練することです。良いトレーニングデータがあれば、このカスタム行列はトレーニングラベルに関連する特徴を強調するのに役立ちます。この行列乗算を（a）埋め込みの修正、または（b）埋め込み間の距離を測定するために使用される距離関数の修正として考えることができ

ます。