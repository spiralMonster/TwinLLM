from loguru import logger

from document_categories.vectordb_document_categories.cleaned_documents.base.cleaned_document import CleanedDocument
from document_categories.vectordb_document_categories.chunked_documents.base.chunked_document import ChunkedDocument

from data_preprocessors.data_chunkers.dispatcher.chunking_handler import ChunkingHandler

from document_categories.data_category import DataCategory


class ChunkingDispatcher:
    chunking_handler=ChunkingHandler()

    @classmethod
    def dispatch(cls,cleaned_document:CleanedDocument) -> list[ChunkedDocument]|None:
        category_name=cleaned_document.get_category()
        data_category=DataCategory(category_name)

        handler=cls.chunking_handler.create_handler(data_category=data_category)

        chunked_docs=handler.chunk(cleaned_document=cleaned_document)

        if chunked_docs:
            num_chunks=len(chunked_docs)
            chunk=chunked_docs[0]

            logger.info(
                f"""
                USER: [{chunk.author_full_name}]
                PLATFORM: [{chunk.platform}]
                LINK: [{chunk.link}]
                CLEANED_DOCUMENT_ID: [{chunk.document_id}]
                INFO: Cleaned Document successfully chunked into {num_chunks} chunks.
                """
            )

            return chunked_docs

        else:
            logger.info("Failed to chunk the cleaned document.")
            logger.info("No chunks returned by Data Chunker.")

            return None