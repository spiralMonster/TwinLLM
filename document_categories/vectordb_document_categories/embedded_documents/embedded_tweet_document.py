from document_categories.vectordb_document_categories.embedded_documents.embedded_document import EmbeddedDocument
from document_categories.data_category import DataCategory


class EmbeddedTweetDocument(EmbeddedDocument):
    username:str|None = None
    link:str|None = None
    published_date:str|None = None


    class Config:
        collection_name="embedded_tweets"
        category=DataCategory.TWEETS
        use_vector_index=True