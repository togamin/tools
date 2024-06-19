# Dockerfile
# ベースイメージとして公式のPythonイメージを使用
FROM python:3.9-slim

# 作業ディレクトリを作成
WORKDIR /app/pomodoro_timer

# カレントディレクトリの内容をコンテナ内の/appにコピー
COPY . /app/pomodoro_timer

# コマンドを実行してアプリを起動
CMD ["python", "pomodoro_timer.py"]