from document_categories.data_category import DataCategory
from document_categories.nosql_db_document_categories.base_document import Document


class ArticleDocument(Document):
    username:str|None = None
    title:str|None = None
    description:str|None = None
    link: str|None = None
    published_date: str|None = None

    class Settings:
        collection_name=DataCategory.ARTICLES