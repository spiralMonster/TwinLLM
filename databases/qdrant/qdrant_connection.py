from loguru import logger
from qdrant_client import QdrantClient
from qdrant_client.http.exceptions import UnexpectedResponse

from settings import Settings

from utils.exceptions.qdrant_exceptions.qdrant_connection_exception import QdrantConnectionException



class QdrantDatabaseConnector:
    _instance: QdrantClient|None = None

    def __new__(cls,*args,**kwargs) -> QdrantClient|None:
        if cls._instance is None:
            try:
                if Settings.USE_QDRANT_CLOUD:
                    instance=QdrantClient(
                        url=Settings.QDRANT_CLOUD_URL,
                        api_key=Settings.QDRANT_API_KEY
                    )
                    cls._instance=instance

                    uri=Settings.QDRANT_CLOUD_URL

                else:
                    instance=QdrantClient(
                        host=Settings.QDRANT_DATABASE_HOST,
                        port=Settings.QDRANT_DATABASE_PORT
                    )
                    cls._instance=instance

                    uri=f"{Settings.QDRANT_DATABASE_HOST}:{Settings.QDRANT_DATABASE_PORT}"


                logger.info(f"Connected successfully to Qdrant Database with uri: {uri}")


            except UnexpectedResponse:
                logger.exception(
                    "Failed to connect to Qdrant Database.",
                    host=Settings.QDRANT_DATABASE_HOST,
                    port=Settings.QDRANT_DATABASE_PORT,
                    url=Settings.QDRANT_CLOUD_URL
                )

                raise QdrantConnectionException("Failed to connect to Qdrant Database.")


        return cls._instance



connection=QdrantDatabaseConnector()