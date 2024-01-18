```
🚨🚨🚨 古い情報があるので注意 🚨🚨🚨
```

# 構成

レコメンドシステムはインデックスやモデルを構築・更新する indexer と indexer が作成した Index を利用して検索を行う Web アプリケーションである searcher から構成されています。

# indexer

Cloud Run Job で定期実行するために利用します。

# searcher

Cloud Run Service で WebAPI サーバとして利用します。

デバッグサーバは以下の通り起動します。
（model の学習が必要なので searcher.build で model を学習&保存してから検索サーバを起動する）

```
python -m searcher.build # Indexなどをダウンロードする
uvicorn searcher.app:app --host 0.0.0.0 --port 8000 --reload
```

または以下でも起動できます。

```
sh dev.sh
```

## Docker

searcher の docker build, docker run は以下のように実行します。

```
docker build -f searcher/Dockerfile -t tbsten/minshumi-search-searcher .

docker run -p 8000:8000 -t tbsten/minshumi-search-searcher

```

タグを変更したい場合は以下のように書くと良さそうです。

```
DOCKER_IMAGE_TAG=タグ
docker build -f searcher/Dockerfile --build-arg GCS_BUCKET=アップロードするGCSバケット -t $DOCKER_IMAGE_TAG .

docker run -p 8000:8000 -t $DOCKER_IMAGE_TAG
```

# 環境変数

```

GOOGLE_APPLICATION_CREDENTIALS=
GCS_BUCKET=
DATABASE_URL=

```
