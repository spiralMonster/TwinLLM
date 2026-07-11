from loguru import logger
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

from settings import Settings


class MongoDBConnector:
    _instance: MongoClient|None = None

    def __new__(cls,*args,**kwargs) -> MongoClient|None:
        if cls._instance is None:
            try:
                cls._instance=MongoClient(Settings.MONGODB_DATABASE_HOST)

            except ConnectionFailure as e:
                logger.error(f"Couldn't connect to the Mongodb server due to error: {e}")

                raise

        logger.info(f"Successfully connected to Mongodb server: {Settings.MONGODB_DATABASE_HOST}")

        return cls._instance

connection=MongoDBConnector()


