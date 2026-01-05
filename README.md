
## 目次

1. [開発環境について](#開発環境について)
2. [URL構成](#URL構成)
3. [アーキテクチャ等で意識した点](#アーキテクチャ等で意識した点)

## 開発環境について

### 前提
dockerが利用できる環境であること。
もしdockerがない場合はdockerをインストールしてください。
[Docker Desktop のインストール](https://docs.docker.jp/desktop/install.html)

### 初期起動まで

1. `git clone https://github.com/rinp/learn_python.git`
1. `cd learn_python`
1. `docker compose up --build -d`
1. `chmod +x ./scripts/*`
1. `./scripts/uv.sh run alembic upgrade head`

[http://localhost:8000/docs](http://localhost:8000/docs)が表示できれば正常に起動できています。

### 開発時向けのスクリプト

ruffを用いたフォーマット等実行スクリプト
```./scripts/check.sh``` 
  
Unit Test実行スクリプト  
```./scripts/test.sh```  
  
uvを用いた処理  
```./scripts/uv.sh <argument>```  

使用例  
`./scripts/uv.sh add fastapi --extra standard`  
`./scripts/uv.sh run alembic init alembic`  
`./scripts/uv.sh run alembic revision --autogenerate -m"comment"`  
`./scripts/uv.sh run alembic upgrade head`  

### その他環境構築

#### Visual Studio CodeおよびDev Containersまわり
現在整理中

#### Pythonのインストールした上での環境構築
上記までの開発環境構築はpythonをローカルPCにインストールしない前提となります。
uvをインストールから以下の手順に沿って処理を進めてください。  
  
またuvのインストールについては複数あるため、必要に応じて切り替えてください。  
[uv公式サイト](https://docs.astral.sh/uv/getting-started/installation/)  

1. `brew install uv`
1. `uv python install`
1. `uv python update-shell`
1. `uv venv`
1. `source .venv/bin/activate`
1. 手動作業 alembic.ini の　sqlalchemy.url についてlocal向けに切り替え(ファイル内にコメント記載あり)
1. `docker compose -f docker-compose-local.yml up --build -d`
1. `uv run alembic upgrade head`
1. `uv sync --frozen`
1. `uv run uvicorn app.main:app --host :: --port 8001 --reload --log-level debug --access-log`

[http://localhost:8001/docs](http://localhost:8001/docs)が表示できれば正常に起動できています。

### フォルダ構成説明

- `app/`: アプリケーション本体。
  - `app/routers/`:FastAPIのルーター
  - `app/schemas/`: リクエスト・レスポンス定義
  - `app/services/`: サービス層
  - `app/crud/`: CRUD層
  - `app/models/`:DBモデル
- `alembic/`: データベースマイグレーション用の設定とバージョン管理スクリプト
- `tests/`: pytest用のユニットテスト群
- `scripts/`: 開発／運用用スクリプト
- `page/`: ドキュメントや OpenAPI の静的出力（`openApi/`）を配置する。
- `htmlcov/`: テストカバレッジのHTML出力。


## URL構成

| URL | Method | 概要 | 主なステータス |
| --- | --- | --- | --- |
| /authors | POST | 著者を作成する | 201, 422 |
| /books | GET | 登録済み書籍を全件取得する | 200 |
| /books | POST | 書籍を作成する（既存の著者が必要） | 201, 404, 422 |
| /books/{book_id} | GET | 1件の書籍を取得する | 200, 404, 422 |
| /books/{book_id} | DELETE | 1件の書籍を削除する | 204, 404, 422 |

より詳細については [https://rinp.github.io/learn_python/api](https://rinp.github.io/learn_python/api) からも確認できます。



### アクセス方法
アプリが起動できている場合は、[http://localhost:8000/docs](http://localhost:8000/docs)等に詳細が表示されますので、そちらも参考にしてください。

著者の登録

```
curl -X 'POST' \
  'http://localhost:8000/authors' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "name": "著者の氏名"
}'
```

書籍の取得
```
curl -X 'GET' \
  'http://localhost:8000/books' \
  -H 'accept: application/json'
```

書籍の削除

```
curl -X 'DELETE' \
  'http://localhost:8000/books/cde621a8-e6e9-11f0-a70b-1e1ecdf371e1' \
  -H 'accept: */*'
```

## アーキテクチャ等で意識した点

### docker
ユーザーごとの環境差も無視できるようにruffやtestに関して前提となるDockerで処理をさせるスクリプトを用意し即時的な対応も可能な状態とした。  
またユニットテスト時のみのデータベースの用意などが容易である点も積極的に活用した。  

### FastAPI
FastAPIでの実装面でもユニットテスト向けに各層ごとに分離がなされるようにした。  
特にFastAPIのDependsはSpring Bootの依存性注入(DI)とは異なり値を返すことという差異について試行錯誤を重ねた。  
サービスの処理をDIしてしまうとリクエストパラメーター等がルーターとなる関数の引数から消えてしまうことから、サービスの処理自体をルーターが受け取る形にした。  
これによりpytestでの```dependency_overrides```での置き換えがスムーズに実装できる形にできた。  
