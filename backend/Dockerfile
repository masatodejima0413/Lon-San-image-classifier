# Python 3.9ベースの軽量コンテナを使用
FROM python:3.9-slim

# 作業ディレクトリ作成
WORKDIR /app

# 依存ファイルをコピー
COPY requirements.txt .

# パッケージをインストール
RUN pip install --upgrade pip && pip install -r requirements.txt

# 残りのファイルをコピー
COPY . .

# APIサーバー起動
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]