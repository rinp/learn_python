## 開発の開始

docker compose up --build -d

http://localhost:8000/docs

## Ruff / Mypy（ローカルにPython不要）

Docker上でRuff/Mypyを実行します（仮想環境はnamed volumeに作成されます）。

- フォーマット + Lint + 型チェック: `./scripts/check.sh`

### uv

#### 初期化
```docker run --rm -it -v"$PWD":/app -w /app astral/uv:0.9.18-python3.14-trixie-slim uv init```

docker run --rm -it -v"$PWD":/app -w /app astral/uv:0.9.18-python3.14-trixie-slim uv venv 

#### パッケージ追加
docker run --rm -it -v"$PWD":/app -w /app astral/uv:0.9.18-python3.14-trixie-slim uv add fastapi --extra standard


### alembic 
docker run --rm -it -v"$PWD":/app -w /app astral/uv:0.9.18-python3.14-trixie-slim uv run --link-mode=copy alembic init alembic

docker run --rm -it -v"$PWD":/app -w /app astral/uv:0.9.18-python3.14-trixie-slim uv run --link-mode=copy alembic revision -m"create tables" 

docker run --rm -it -v"$PWD":/app -w /app astral/uv:0.9.18-python3.14-trixie-slim uv run --link-mode=copy alembic upgrade head 

# 学び
## uv
pipと比較し高速であるパッケージマネージャー。
コンテナでの開発のためpyenvのような機能は実際には使用することなく、速度だけを重視した採用。

dockerを経由してローカルには何もインストールせずに利用する想定で作成をすすめるが、
pythonを普段使いするのであればuvをインストールの上で、version指定もすることで優位性がさらに高いと考えられる。

### TODO
alembicでのdbコンテナへの指定について



class Base(DeclarativeBase):
    # pass
    __abstract__ = True # このクラスはテーブルとして作成されない

    # TODO 備忘録：各クラス共通項目の書き方、あとで別に記載
    # created_at: Mapped[datetime] = mapped_column(
    #     DateTime, default=func.now(), nullable=False
    # )
    # updated_at: Mapped[datetime] = mapped_column(
    #     DateTime, default=func.now(), onupdate=func.now(), nullable=False
    # )
 
