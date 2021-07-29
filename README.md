#FastAPI pet project with Tortoise-ORM and Aerich

This project uses Tortoise-ORM and Aerich as a database migrations tool.

##Aerich migrations
You need add aerich.models to your Tortoise-ORM config first. Example:
```python
TORTOISE_ORM = {
    "connections": {"default": "mysql://root:123456@127.0.0.1:3306/test"},
    "apps": {
        "models": {
            "models": ["tests.models", "aerich.models"],
            "default_connection": "default",
        },
    },
}
```

##Some base Aerich commands, see [docs](https://github.com/tortoise/aerich/blob/dev/README.md) for details.

###Initialization

```shell
aerich init -t tests.backends.mysql.TORTOISE_ORM
```

###Init db
```shell
aerich init-db
```

###Update models and make migrate
```shell
aerich migrate 
```

###Upgrade to latest version
```shell
aerich upgrade
```

###Downgrade
```shell
aerich downgrade
```