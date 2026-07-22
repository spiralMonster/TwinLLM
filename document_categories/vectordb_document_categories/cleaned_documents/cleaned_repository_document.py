from document_categories.vectordb_document_categories.cleaned_documents.base.cleaned_document import CleanedDocument
from document_categories.data_category import DataCategory


class CleanedRepositoryDocument(CleanedDocument):
    repository_name:str|None = None
    link:str|None = None
    file_name:str|None = None
    programming_language_used:str|None = None


    class Config:
        collection_name="cleaned_repository"
        category=DataCategory.REPOSITORIES
        use_vector_index=False
