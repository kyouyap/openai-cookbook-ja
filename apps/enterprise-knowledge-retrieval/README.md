# 企業向け知識検索

このアプリケーションは、非構造化テキスト文書を取り扱い、それを使用可能な知識ベースアプリケーションに変換することを目指す、企業向け知識検索に関する詳細な調査です。

このリポジトリにはノートブックと基本的なStreamlitアプリが含まれています：
- `enterprise_knowledge_retrieval.ipynb`：データのトークン化、チャンキング、埋め込みを段階的に実行し、ベクトルデータベースに知識を構築し、それを基にチャットエージェントを構築し、その性能を基本的に評価するプロセスが記述されたノートブックです。
- `chatbot.py`：知識ベースへのクエリを通じたシンプルなQ&Aを提供するStreamlitアプリです。

アプリを実行するには、以下の「App」セクションに記載された手順に従ってください。

## ノートブック

ノートブックは最適なスタート地点であり、シンプルなバックエンド知識検索サービスの設定と評価を行うためのエンドツーエンドのワークフローを紹介します：
- **セットアップ：** 変数の初期化およびベクトルデータベースへの接続。
- **ストレージ：** データベースの設定、データの準備、埋め込みと検索用のメタデータの格納。
- **検索：** 基本的な検索機能を備えた関連文書の抽出、および結果を簡潔な回答に要約するためのLLMの使用。
- **回答：** ユーザーのクエリを処理し、フォローアップの質問に対応するための高度なエージェントの追加。
- **評価：** サービスを使用して質問/回答ペアを受け取り、それらを評価し、対策のためにプロットします。

ノートブックを「Search」ステージまで実行したら、アプリを設定して実行するために必要なものが揃います。

## アプリ

標準の意味論的検索または[HyDE](https://arxiv.org/abs/2212.10496)検索を使用して、検索サービスをテストするために対話できる基本的なStreamlitアプリを組み込んでいます。

使用方法：
- ノートブックからセットアップとストレージの手順に従い、検索可能なコンテンツを含むベクトルデータベースを準備します。
- `virtualenv`がインストールされていることを確認し、`virtualenv venv`を実行して仮想環境を設定します。
- 仮想環境をアクティブにするには、`source venv/bin/activate`を実行します。
- `pip install -r requirements.txt`を実行して必要なパッケージをインストールします。
- ブラウザでStreamlitアプリを起動するには、`streamlit run chatbot.py`を実行します。

## 制限事項

- このアプリはベクトルデータベースとしてRedisを使用していますが、必要に応じて他のオプションが`../examples/vector_databases`で示されています。
- ノートブックでは最適化の余地が多く紹介されていますが、これらについては後続のクックブックで詳しく説明します。