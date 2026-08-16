from datetime import datetime,timezone
from pydantic import Field
from loguru import logger

from qdrant_client.http import exceptions
from qdrant_client.models import PayloadSchemaType,OrderBy,Direction
from databases.qdrant.qdrant_connection import connection

from document_categories.vectordb_document_categories.base.vector_base_document import VectorBaseDocument
from document_categories.data_category import DataCategory
from utils.exceptions.qdrant_exceptions.document_insertion_exception import DocumentInsertionException

class ConversationHistoryDocument(VectorBaseDocument):
    conversation:str
    published_at:datetime=Field(default_factory=lambda:datetime.now(timezone.utc))

    class Config:
        collection_name:str="conversation_history"
        category:str=DataCategory.CONVERSATION_HISTORY
        use_vector_index:bool=False


    @classmethod
    def create_published_at_index(cls) -> None:
        collection_name=cls.get_collection_name()

        connection.create_payload_index(
            collection_name=collection_name,
            field_name="published_at",
            field_schema=PayloadSchemaType.DATETIME
        )



    @classmethod
    def bulk_insert(cls,documents:list["ConversationHistoryDocument"]) -> bool:
        try:
            cls._bulk_insert(documents=documents)

        except exceptions.UnexpectedResponse:
            collection_name=cls.get_collection_name()
            logger.info(f"Collection name: {collection_name} does not exist. Creating the collection and then inserting the documents.")
            logger.info("Creating the 'published_at' index.")

            cls.create_collection()
            cls.create_published_at_index()
            try:
                cls._bulk_insert(documents=documents)

            except exceptions.UnexpectedResponse:
                logger.error("Failed to insert the documents.")
                raise DocumentInsertionException("Failed to insert the documents in Database.")

            return True

        return True


    @classmethod
    def get_num_points_in_collection(cls) ->int:
        collection_name=cls.get_collection_name()
        try:
            collection_info=connection.get_collection(
                collection_name=collection_name
            )
            num_documents=collection_info.points_count

        except Exception as e:
            logger.info(f"Exception encountered: {e}")
            num_documents=0

        return num_documents


    @classmethod
    def get_latest_conversations(cls,limit:int,**kwargs) -> list["ConversationHistoryDocument"]:
        collection_name=cls.get_collection_name()

        with_payload=kwargs.pop("with_payload",True)
        with_vectors=kwargs.pop("with_vectors",False)

        num_documents_in_collection=cls.get_num_points_in_collection()
        if num_documents_in_collection<=limit:
            records,_=connection.scroll(
                collection_name=collection_name,
                limit=num_documents_in_collection,
                with_payload=with_payload,
                with_vectors=with_vectors,
                **kwargs
            )

        else:
            records,_=connection.scroll(
                collection_name=collection_name,
                limit=limit,
                order_by=OrderBy(
                    key="published_at",
                    direction=Direction.DESC
                ),
                with_payload=with_payload,
                with_vectors=with_vectors,
                **kwargs
            )


        result=[
            cls.from_record(record)
            for record in records
        ]
        return result








