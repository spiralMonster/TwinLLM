from abc import ABC, abstractmethod

from document_categories.nosql_db_document_categories.no_sql_base_document import NoSQLBaseDocument

class BaseCrawler(ABC):
    document_model: type[NoSQLBaseDocument]

    @abstractmethod
    def extract(self,link:str,**kwargs) -> tuple[str,dict]:
        pass

