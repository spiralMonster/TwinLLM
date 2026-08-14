from loguru import logger
from qdrant_client.models import Filter

from document_categories.vectordb_document_categories.chunked_documents.repository_chunked_document import RepositoryChunkedDocument
from document_categories.vectordb_document_categories.embedded_documents.embedded_repository_document import EmbeddedRepositoryDocument

from data_preprocessors.data_embedders.repository_data_embedder import RepositoryDataEmbedder


def filtered_vector_search_over_repositories(
        query:str,
        documents_to_retrieved:int,
        filters:Filter|None
) -> list[EmbeddedRepositoryDocument]:
    logger.info("Performing Filtered Vector Search over Repository collections.")

    query_chunk=RepositoryChunkedDocument(
        content=query
    )

    embedded_query=RepositoryDataEmbedder().embed(chunk=query_chunk)

    retrieved_documents=EmbeddedRepositoryDocument.search(
        query_vector=embedded_query.embedding,
        limit=documents_to_retrieved,
        query_filter=filters
    )

    return retrieved_documents