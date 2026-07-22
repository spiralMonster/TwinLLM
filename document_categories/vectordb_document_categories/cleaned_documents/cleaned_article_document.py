from document_categories.vectordb_document_categories.cleaned_documents.base.cleaned_document import CleanedDocument
from document_categories.data_category import DataCategory



class CleanedArticleDocument(CleanedDocument):
    username:str|None = None
    title:str|None = None
    description:str|None = None
    link:str|None = None
    published_date:str|None = None


    class Config:
        collection_name="cleaned_articles"
        category=DataCategory.ARTICLES
        use_vector_index=False