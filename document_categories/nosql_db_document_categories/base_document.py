from abc import ABC
from pydantic import UUID4,Field

from document_categories.nosql_db_document_categories.no_sql_base_document import NoSQLBaseDocument


class Document(NoSQLBaseDocument,ABC):
    content: dict
    platform: str
    author_id: UUID4 = Field(alias="author_id")
    author_full_name: str = Field(alias="author_full_name")

    class Settings:
        collection_name: str = "documents"