from pydantic import UUID4,Field
from document_categories.vectordb_document_categories.base.vector_base_document import VectorBaseDocument

from document_categories.data_category import DataCategory


class Query(VectorBaseDocument):
    content:str
    query_type:set[str]|None=None
    author_id:UUID4|None=None
    author_full_name:str|None=None
    metadata:dict=Field(default_factory=dict)

    class Config:
        category=DataCategory.QUERIES


    @classmethod
    def from_str(cls,content:str) -> "Query":
        content=content.strip()
        content=content.strip("\n")

        query=Query(
            content=content
        )

        return query


    def replace_content(self,new_content:str) -> "Query":
        query=Query(
            content=new_content,
            query_type=self.query_type,
            author_id=self.author_id,
            author_full_name=self.author_full_name,
            metadata=self.metadata
        )

        return query