from document_categories.rag_document_categories.query_document import Query
from document_categories.data_category import DataCategory


class EmbeddedQuery(Query):
    embedding:list[float]

    class Config:
        category=DataCategory.QUERIES