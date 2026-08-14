from loguru import logger
from qdrant_client.models import Filter

from document_categories.vectordb_document_categories.chunked_documents.tweet_chunked_document import TweetChunkedDocument
from document_categories.vectordb_document_categories.embedded_documents.embedded_tweet_document import EmbeddedTweetDocument

from data_preprocessors.data_embedders.tweet_data_embedder import TweetDataEmbedder


def filtered_vector_search_over_tweets(
        query:str,
        documents_to_retrieved:int,
        filters:Filter|None
) -> list[EmbeddedTweetDocument]:
    logger.info("Performing Filtered Vector Search over Tweet collections.")

    query_chunk=TweetChunkedDocument(
        content=query
    )

    embedded_query=TweetDataEmbedder().embed(chunk=query_chunk)

    retrieved_documents=EmbeddedTweetDocument.search(
        query_vector=embedded_query.embedding,
        limit=documents_to_retrieved,
        query_filter=filters
    )

    return retrieved_documents