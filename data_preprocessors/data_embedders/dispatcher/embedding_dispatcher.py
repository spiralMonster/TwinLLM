from loguru import logger

from document_categories.vectordb_document_categories.chunked_documents.base.chunked_document import ChunkedDocument
from document_categories.vectordb_document_categories.embedded_documents.base.embedded_document import EmbeddedDocument

from data_preprocessors.data_embedders.dispatcher.embedding_handler import EmbeddingHandler

from document_categories.data_category import DataCategory


class EmbeddingDispatcher:
    embedding_handler=EmbeddingHandler()

    @classmethod
    def dispatch(cls,chunked_documents:list[ChunkedDocument]) -> list[EmbeddedDocument]|None:
        chunk=chunked_documents[0]
        category_name=chunk.get_category()
        data_category=DataCategory(category_name)

        handler=cls.embedding_handler.create_handler(data_category=data_category)

        embedded_docs=handler.embed_batch(chunked_data=chunked_documents)

        if embedded_docs:
            num_embedd_docs=len(embedded_docs)
            embed_doc=embedded_docs[0]

            logger.info(
                f"""
                USER: [{embed_doc.author_full_name}]
                PLATFORM: [{embed_doc.platform}]
                LINK: [{embed_doc.link}]
                DOCUMENT_ID: [{embed_doc.document_id}]
                INFO: {num_embedd_docs} Chunked documents converted to Embedded Docs.
                """
            )

            return embedded_docs

        else:
            logger.info("Failed to embedd the chunked document.")
            logger.info("No embedded documents returned by Data Embedder.")

            return None

