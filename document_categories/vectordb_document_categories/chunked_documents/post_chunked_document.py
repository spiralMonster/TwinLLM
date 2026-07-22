from document_categories.vectordb_document_categories.chunked_documents.base.chunked_document import ChunkedDocument
from document_categories.data_category import DataCategory


class PostChunkedDocument(ChunkedDocument):
    username:str|None = None
    link:str|None = None
    published_date:str|None = None


    class Config:
        collection_name="post_chunks"
        category=DataCategory.POSTS
        use_vector_index=False

