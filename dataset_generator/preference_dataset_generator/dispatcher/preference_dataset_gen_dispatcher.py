from document_categories.vectordb_document_categories.chunked_documents.base.chunked_document import ChunkedDocument
from document_categories.preference_dataset_document_categories.base.preference_document import PreferenceDocument

from dataset_generator.preference_dataset_generator.dispatcher.preference_dataset_gen_handler import PreferenceDatasetGenHandler

from document_categories.data_category import DataCategory


class PreferenceDatasetGenDispatcher:
    handler_class=PreferenceDatasetGenHandler()

    @classmethod
    def dispatch(cls,chunked_documents:list[ChunkedDocument]) -> list[PreferenceDocument]:
        chunk=chunked_documents[0]

        category=chunk.get_category()
        data_category=DataCategory(category)

        handler=cls.handler_class.create_handler(data_category=data_category)
        preference_docs=handler.generate(chunked_documents=chunked_documents)

        return preference_docs