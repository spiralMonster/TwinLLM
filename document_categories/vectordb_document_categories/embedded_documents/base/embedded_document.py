from abc import ABC
from pydantic import Field,UUID4

from document_categories.vectordb_document_categories.base.vector_base_document import VectorBaseDocument


class EmbeddedDocument(VectorBaseDocument,ABC):
    content:str
    embedding: list[float]|None
    platform:str
    document_id:UUID4
    author_id:UUID4
    author_full_name:str
    metadata:dict = Field(default_factory=dict)


    class Config:
        category: str
        collection_name: str
        use_vector_index: bool