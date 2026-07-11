from typing import Optional

from document_categories.nosql_db_document_categories.base_document import Document
from document_categories.data_category import DataCategory


class PostDocument(Document):
    username: str|None = None
    image: Optional[str] = None
    link: str|None = None
    published_date: str|None = None

    class Settings:
        collection_name=DataCategory.POSTS
