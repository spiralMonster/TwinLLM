from abc import ABC
from pydantic import UUID4

from document_categories.vectordb_document_categories.vector_base_document import VectorBaseDocument


class CleanedDocument(VectorBaseDocument,ABC):
    content: str
    platform: str
    author_id: UUID4
    author_full_name: str

