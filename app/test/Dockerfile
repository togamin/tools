# Dockerfile
# ベースイメージとして公式のPythonイメージを使用
FROM python:3.9-slim

# 作業ディレクトリを作成
WORKDIR /app/test

# カレントディレクトリの内容をコンテナ内の/appにコピー
COPY . /app/test

# コマンドを実行してアプリを起動
CMD ["python", "app.py"]
