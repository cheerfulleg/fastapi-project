#FastAPI pet project 

**Goals**:
 - to try new framework [FastAPI](https://fastapi.tiangolo.com/) and to implement basic CRUD operations; ✔️
 - to try [TortoiseORM](https://fastapi.tiangolo.com/) and [Aerich](https://github.com/tortoise/aerich/blob/dev/README.md) as a database migrations tool; ✔️
 - to try using [Celery](https://docs.celeryproject.org/en/stable/) + Redis with FastAPI and to implement all types of relations; ✔️
 - to work with files: save files to [AWS S3](https://aws.amazon.com/s3/) bucket; ✔️
 - to cover endpoints with tests using [pytest](https://docs.pytest.org/en/6.2.x/); ✔️
 - to implement simple chat using [MongoDB](https://www.mongodb.com/) and websockets; ✔️
 - to implement [caching queries](https://pypi.org/project/fastapi-cache2/) with Redis; ✔️
 - to integrate [black](https://github.com/psf/black), [flake8](https://flake8.pycqa.org/en/latest/) formatting on [pre-commit](https://pre-commit.com/). ✔️
 
**ENVIRONMENT VARIABLES:**

Postgres Configs:
- DB_USER
- DB_PASS
- DB_HOST
- DB_NAME

JWT Auth Configs:
- JWT_SECRET
- ACCESS_TOKEN_EXP_MINUTES
- REFRESH_TOKEN_EXP_HOURS

Email Configs:
- EMAIL_HOST_USER
- EMAIL_HOST_PASSWORD

AWS S3 Configs:
- AWS_ACCESS_KEY
- AWS_SECRET_ACCESS_KEY
- AWS_REGION
- S3_BUCKET

Celery Redis Broker:
- CELERY_BROKER_URL

Redis Cache:
- REDIS_CACHE_URL

MongoDB Configs:
- MONGODB_URL


**Start project**

```shell
python run.py
```

**Testing**

Run tests:
```shell
run_tests.sh
```