## 開発の開始

docker compose up --build -d

### uv

#### 初期化
```docker run --rm -it -v"$PWD":/app -w /app astral/uv:0.9.18-python3.14-trixie-slim uv init```

#### パッケージ追加
docker run --rm -it -v"$PWD":/app -w /app astral/uv:0.9.18-python3.14-trixie-slim uv add fastapi --extra standard


# 学び
## uv
pipと比較し高速であるパッケージマネージャー。
コンテナでの開発のためpyenvのような機能は実際には使用することなく、速度だけを重視した採用。

dockerを経由してローカルには何もインストールせずに利用する想定で作成をすすめるが、
pythonを普段使いするのであればuvをインストールの上で、version指定もすることで優位性がさらに高いと考えられる。


