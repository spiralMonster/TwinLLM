from document_categories.vectordb_document_categories.embedded_documents.base.embedded_document import EmbeddedDocument
from document_categories.data_category import DataCategory



class EmbeddedPostDocument(EmbeddedDocument):
    username:str|None = None
    link:str|None = None
    published_date:str|None = None


    class Config:
        collection_name="embedded_posts"
        category=DataCategory.POSTS
        use_vector_index=True

