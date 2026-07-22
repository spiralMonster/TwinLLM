from document_categories.vectordb_document_categories.embedded_documents.base.embedded_document import EmbeddedDocument
from document_categories.data_category import DataCategory


class EmbeddedArticleDocument(EmbeddedDocument):
    username:str|None
    title:str|None
    description:str|None
    published_date:str|None


    class Config:
        collection_name="embedded_articles"
        category=DataCategory.ARTICLES
        use_vector_index=True
