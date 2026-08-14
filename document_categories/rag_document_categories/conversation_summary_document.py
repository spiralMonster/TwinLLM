from loguru import logger
from typing import Any

from document_categories.vectordb_document_categories.base.vector_base_document import VectorBaseDocument
from document_categories.data_category import DataCategory

from qdrant_client.models import PointIdsList
from databases.qdrant.qdrant_connection import connection


class ConversationSummaryDocument(VectorBaseDocument):
    summary:str

    class Config:
        collection_name:str="conversation_summary"
        category:str=DataCategory.CONVERSATION_SUMMARY
        use_vector_index:bool=False


    @classmethod
    def get_num_points_in_collection(cls) -> int:
        collection_name=cls.get_collection_name()
        try:
            collection_info=connection.get_collection(
                collection_name=collection_name
            )
            num_points=collection_info.points_count

        except Exception as e:
            logger.info(f"Exception Encountered: {e}")
            num_points=0

        return num_points


    @classmethod
    def retrieve_point(cls,**kwargs) -> "ConversationSummaryDocument":
        collection_name=cls.get_collection_name()

        with_payload=kwargs.pop("with_payload",True)
        with_vectors=kwargs.pop("with_vectors",False)

        records,_=connection.scroll(
            collection_name=collection_name,
            limit=1,
            with_payload=with_payload,
            with_vectors=with_vectors
        )

        point=records[0]
        doc=cls.from_record(point=point)

        return doc


    @classmethod
    def update_point(cls,point_id:str,attribute:str,updated_value:Any) -> None:
        collection_name=cls.get_collection_name()

        connection.set_payload(
            collection_name=collection_name,
            payload={
                attribute:updated_value
            },
            points=PointIdsList(
                points=[point_id]
            )
        )
