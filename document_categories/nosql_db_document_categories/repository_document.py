from document_categories.data_category import DataCategory
from document_categories.nosql_db_document_categories.base.base_document import Document


class RepositoryDocument(Document):
    content: dict|None = None
    repository_name: str|None = None
    link: str|None = None
    file_count: int|None = None
    programming_languages_used: str|None = None

    class Settings:
        collection_name=DataCategory.REPOSITORIES


