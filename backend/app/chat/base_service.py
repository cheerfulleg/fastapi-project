from typing import TypeVar, Type

from motor.motor_asyncio import AsyncIOMotorCollection

Collection = TypeVar("Collection", bound=AsyncIOMotorCollection)


class BaseService:
    """
    Wrapper to make queries in Django styled way
    """

    collection: Type[Collection]

    @classmethod
    async def create(cls, data: dict) -> dict:
        """
        Create object method

        :param data: data to pass to the object
        :return: bson type dict
        """
        created_object = await cls.collection.insert_one(data)
        return await cls.collection.find_one({"_id": created_object.inserted_id})

    @classmethod
    async def get(cls, query_params: dict) -> dict:
        """
        Get object by id

        :param query_params: MongoDB typed parameters
        :return: bson type dict
        """
        return await cls.collection.find_one(query_params)

    @classmethod
    async def get_or_create(cls, query_params: dict, default: dict) -> dict:
        """
        Combination of get and create methods. Create new object if it wasn't found

        :param query_params: MongoDB typed parameters
        :param default: data to pass to the object if not exists
        :return: bson type dict
        """
        if obj := await cls.get(query_params):
            return obj
        else:
            return await cls.create(default)

    @classmethod
    async def all(cls) -> list:
        """
        Get all objects in collection

        :return: list of bson type dicts
        """
        result = []
        async for obj in cls.collection.find():
            result.append(obj)
        return result

    @classmethod
    async def update(cls, query_params: dict, payload: dict) -> dict:
        """
        Update object

        :param query_params: MongoDB typed parameters
        :param payload: data to update
        :return: bson type dict
        """
        obj = {k: v for k, v in payload.items() if v is not None}
        if len(obj) >= 1:
            update_result = await cls.collection.update_one(query_params, {"$set": obj})
            if update_result.modified_count == 1:
                return await cls.get(query_params)

    @classmethod
    async def delete(cls, query_params: dict) -> bool:
        """
        Delete object

        :param query_params: MongoDB typed parameters
        :return: True
        """
        delete_result = await cls.collection.delete_one(query_params)
        if delete_result.deleted_count == 1:
            return True

    @classmethod
    async def filter(cls, filter_params: dict) -> list:
        """
        Filter objects by filter parameters

        :param filter_params: MongoDB typed parameters
        :return: list of bson typed dicts
        """
        result = []
        async for obj in cls.collection.find(filter_params):
            result.append(obj)
        return result
