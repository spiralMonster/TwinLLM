from loguru import logger

from document_categories.nosql_db_document_categories.base.base_document import Document
from document_categories.vectordb_document_categories.cleaned_documents.base.cleaned_document import CleanedDocument

from data_preprocessors.data_cleaners.dispatcher.cleaning_handler import CleaningHandler

from document_categories.data_category import DataCategory


class CleaningDispatcher:
    cleaning_handler=CleaningHandler()

    @classmethod
    def dispatch(cls,document:Document) -> CleanedDocument|list[CleanedDocument]|None:
        document_collection=document.get_collection_name()
        data_category=DataCategory(document_collection)

        handler=cls.cleaning_handler.create_handler(data_category=data_category)

        cleaned_document=handler.clean(document_model=document)

        if cleaned_document:
            if not isinstance(cleaned_document,list):
                logger.info(
                    f"""
                    USER: [{cleaned_document.author_full_name}]
                    PLATFORM: [{cleaned_document.platform}]
                    LINK: [{cleaned_document.link}]
                    NUMBER_OF_TOKENS_IN_CLEANED_DOC: [{len(cleaned_document.content.split(" "))}]
                    DOC_LENGTH: [{len(cleaned_document.content)}]
                    INFO: Document Cleaned Successfully.
                    """
                )

            else:
                doc=cleaned_document[0]
                doc_len=len(cleaned_document)
                logger.info(
                    f"""
                    USER: [{doc.author_full_name}]
                    PLATFORM: [{doc.platform}]
                    LINK: [{doc.link}]
                    INFO: {doc_len} Document Files Cleaned Successfully.
                    """
                )


            return cleaned_document

        else:
            logger.info("Failed to clean the document.")
            logger.info("Document's length is less than minimum content length.")

            return None
