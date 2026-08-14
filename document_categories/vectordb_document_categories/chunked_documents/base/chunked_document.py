from abc import ABC
from pydantic import Field,UUID4

from document_categories.vectordb_document_categories.base.vector_base_document import VectorBaseDocument


class ChunkedDocument(VectorBaseDocument,ABC):
    content:str
    platform:str|None=None
    link:str|None=None
    document_id:UUID4|None=None
    author_id:UUID4|None=None
    author_full_name:str|None=None
    metadata:dict|None = Field(default_factory=dict)


    class Config:
        category: str
        collection_name: str
        use_vector_index: bool

