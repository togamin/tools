# Dockerfile
# ベースイメージとして公式のPythonイメージを使用
FROM python:3.9-slim

# 作業ディレクトリを作成
WORKDIR /app

# requirements.txt をコンテナにコピー
COPY requirements.txt /app/

# 依存関係をインストール
 RUN pip install --no-cache-dir -r requirements.txt

# カレントディレクトリの内容をコンテナ内の/appにコピー
COPY . /app

# コマンドを実行してアプリを起動
CMD ["python", "pomodoro_timer.py"]