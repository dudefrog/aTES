# aTES

Advanced Task Exchange System - homework for async architecture course

Note! Code is intentionally insecure and ugly. Don't want to polish the solution under a
time pressure, it's better to have _something_ in a working state

### Pre-requisites:

- Poetry
- docker

## Quick bootstrap

```shell
# will install and bootstrap everything
make install
```

## Auth service

Django application based on
[django-oauth-toolkit](https://django-oauth-toolkit.readthedocs.io/)

### Installation and usage

```
cd task_tracker
make install
make dev
```

## Task tracker service

Django application that is far from perfect.

### Installation and usage

```
cd task_tracker
make install
make dev
```

Consume messages:

```
cd task_tracker
make consume
```

## Message broker

Apache Kafka is used for async messaging. The following command will run Kafka in docker

```shell
docker-compose up
# or
docker-compose up -d
```

## Initial setup

1. Login in [auth service](http://localhost:5000/)
2. Register an [application](http://localhost:5000/o/applications/register/) with
   Confidential type, `code` grant type and callback URL set to
   `http://localhost:8050/oauth/callback`
3. Set client ID and client secret in `task_tracker` settings
4. You're good. Login to [task tracker](http://localhost:8050)
