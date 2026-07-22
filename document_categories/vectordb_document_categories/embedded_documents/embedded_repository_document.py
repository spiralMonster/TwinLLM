from document_categories.vectordb_document_categories.embedded_documents.base.embedded_document import EmbeddedDocument
from document_categories.data_category import DataCategory


class EmbeddedRepositoryDocument(EmbeddedDocument):
    repository_name:str|None
    link:str|None
    file_name:str|None
    programming_language_used:str|None


    class Config:
        collection_name="embedded_repository"
        category=DataCategory.REPOSITORIES
        use_vector_index=True

