from loguru import logger
from qdrant_client.models import Filter

from document_categories.vectordb_document_categories.chunked_documents.post_chunked_document import PostChunkedDocument
from document_categories.vectordb_document_categories.embedded_documents.embedded_post_document import EmbeddedPostDocument

from data_preprocessors.data_embedders.post_data_embedder import PostDataEmbedder


def filtered_vector_search_over_posts(
        query:str,
        documents_to_retrieved:int,
        filters:Filter|None
) -> list[EmbeddedPostDocument]:
    logger.info("Performing Filtered Vector Search over Post collections.")

    query_chunk=PostChunkedDocument(
        content=query
    )

    embedded_query=PostDataEmbedder().embed(chunk=query_chunk)

    retrieved_documents=EmbeddedPostDocument.search(
        query_vector=embedded_query.embedding,
        limit=documents_to_retrieved,
        query_filter=filters
    )

    return retrieved_documents