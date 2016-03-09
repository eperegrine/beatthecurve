# Curvus

Curvus is a project to allow students to share notes and study tips

## Setup

_Todo:_ Write setup instructions

## How to run

Once setup here is how to run the site/server

**Start a postgres server**
```sh
export PGDATA=/usr/local/var/postgres;
postgres;
```

**Start server**
```sh
source venv/bin/activate #Or another way to start the virtual env
export AWS_ACCESS_KEY=AKIAJPAM7ZQCRQQ5GP3Q
export AWS_SECRET_KEY=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
export S3_BUCKET=beatthecurve
export UPLOADS_URL="https://s3-us-west-2.amazonaws.com/beatthecurve/";
export SECRET_KEY=a_secret;
export PG_PASSWORD=;
export REDIS_URL=;
gunicorn --worker-class eventlet app:app --log-file=- -w 1;
```

**Start sass watcher**

_Optional - For style development_
```sh
cd app/static
sass --watch sass/main.scss:css/main.css --style compressed
```

**Start Redis server**
```sh
redis-server
```
