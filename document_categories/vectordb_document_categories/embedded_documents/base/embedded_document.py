from abc import ABC
from pydantic import Field,UUID4

from document_categories.vectordb_document_categories.base.vector_base_document import VectorBaseDocument


class EmbeddedDocument(VectorBaseDocument,ABC):
    content:str
    embedding: list[float]|None
    platform:str|None
    link:str|None
    document_id:UUID4|None
    author_id:UUID4|None
    author_full_name:str|None
    metadata:dict = Field(default_factory=dict)


    class Config:
        category: str
        collection_name: str
        use_vector_index: bool