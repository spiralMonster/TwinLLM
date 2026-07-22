from document_categories.vectordb_document_categories.chunked_documents.chunked_document import ChunkedDocument
from document_categories.data_category import DataCategory


class RepositoryChunkedDocument(ChunkedDocument):
    repository_name:str|None = None
    link:str|None = None
    file_name:str|None = None
    programming_language_used:str|None = None


    class Config:
        collection_name="repository_chunks"
        category=DataCategory.REPOSITORIES
        use_vector_index=False
