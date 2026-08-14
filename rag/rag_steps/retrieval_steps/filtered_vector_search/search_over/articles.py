from loguru import logger
from qdrant_client.models import Filter

from document_categories.vectordb_document_categories.chunked_documents.article_chunked_document import ArticleChunkedDocument
from document_categories.vectordb_document_categories.embedded_documents.embedded_article_document import EmbeddedArticleDocument

from data_preprocessors.data_embedders.article_data_embedder import ArticleDataEmbedder


def filtered_vector_search_over_articles(
        query:str,
        documents_to_retrieved:int,
        filters:Filter|None
) -> list[EmbeddedArticleDocument]:
    logger.info("Performing Filtered Vector Search over Article collections.")

    query_chunk=ArticleChunkedDocument(
        content=query
    )

    embedded_query=ArticleDataEmbedder().embed(chunk=query_chunk)

    retrieved_documents=EmbeddedArticleDocument.search(
        query_vector=embedded_query.embedding,
        limit=documents_to_retrieved,
        query_filter=filters
    )

    return retrieved_documents