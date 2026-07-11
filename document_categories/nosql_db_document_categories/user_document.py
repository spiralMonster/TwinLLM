from document_categories.data_category import DataCategory
from document_categories.nosql_db_document_categories.no_sql_base_document import NoSQLBaseDocument


class UserDocument(NoSQLBaseDocument):
    first_name: str|None = None
    last_name: str|None = None

    class Settings:
        collection_name=DataCategory.USERS


    @property
    def full_name(self):
        f_name=f"{self.first_name} {self.last_name}"

        return f_name