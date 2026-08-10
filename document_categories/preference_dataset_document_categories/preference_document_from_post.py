from document_categories.preference_dataset_document_categories.base.preference_document import PreferenceDocument
from document_categories.data_category import DataCategory


class PreferenceDocumentFromPost(PreferenceDocument):
    class Config:
        data_category=DataCategory.POSTS

