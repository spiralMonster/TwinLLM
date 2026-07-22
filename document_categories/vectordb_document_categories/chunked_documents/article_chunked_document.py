from document_categories.vectordb_document_categories.chunked_documents.chunked_document import ChunkedDocument
from document_categories.data_category import DataCategory


class ArticleChunkedDocument(ChunkedDocument):
    username:str|None = None
    title:str|None = None
    description:str|None = None
    published_date:str|None = None


    class Config:
        collection_name="article_chunks"
        category=DataCategory.ARTICLES
        use_vector_index=False