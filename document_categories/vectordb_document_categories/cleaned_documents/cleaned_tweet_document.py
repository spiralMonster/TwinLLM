from document_categories.vectordb_document_categories.cleaned_documents.base.cleaned_document import CleanedDocument
from document_categories.data_category import DataCategory


class CleanedTweetDocument(CleanedDocument):
    username:str|None = None
    link:str|None = None
    published_date:str|None = None


    class Config:
        collection_name="cleaned_tweets"
        category=DataCategory.TWEETS
        use_vector_index=False