# FIXME

## 課題部分

- ルーターで `response_model` を指定していないため、FastAPI がレスポンススキーマを強制せずドキュメントも不正確になる。OpenAPI の整合性とフィールド漏れ防止のため `response_model=...` を付与する（例: [app/routers/book_router.py](app/routers/book_router.py#L31-L118), [app/routers/author_router.py](app/routers/author_router.py#L21-L40)).
- 開発時ログミドルウェアは非JSONにも対応したが、コンテンツタイプやサイズの判定なしでボディ全量をログ出力するため機密情報やバイナリを誤って吐き出すリスクがある。`Content-Type` チェックとサイズ上限／マスキングを追加すべき ([app/main.py](app/main.py#L28-L47)).

## 対応確認

（下記は修正済み・動作確認は適宜）

### 完了

- 本番運用時に `create_engine(echo=True)` のまま SQL が全量ログ出力される懸念を環境判定で抑制 ([app/database.py](app/database.py#L21-L31)).
- Pydantic 入力 `BookCreateParam` に `extra="forbid"` を付与して余計なフィールドを拒否 ([app/schemas/param.py](app/schemas/param.py#L24-L41)).
- IntegrityError の握りつぶしを防ぎ、外部キー違反以外は再送出するよう修正 ([app/repository/book_crud.py](app/repository/book_crud.py#L45-L67)).
- `author_id` を NOT NULL としてデータ整合性を担保 ([app/models/book.py](app/models/book.py#L21-L32)).
- 例外クラス名の綴りを `*Exception` に修正し統一 ([app/exceptions.py](app/exceptions.py#L7-L32)).
- POST ミドルウェアを非 JSON ボディでも落ちないよう安全なログ化に変更 ([app/main.py](app/main.py#L28-L47)).

## 確認済み