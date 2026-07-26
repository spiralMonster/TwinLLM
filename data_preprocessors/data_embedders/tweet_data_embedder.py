from data_preprocessors.data_embedders.base.data_embedder import DataEmbedder

from document_categories.vectordb_document_categories.chunked_documents.tweet_chunked_document import TweetChunkedDocument
from document_categories.vectordb_document_categories.embedded_documents.embedded_tweet_document import EmbeddedTweetDocument


class TweetDataEmbedder(DataEmbedder):
    def map_model(self,chunk:TweetChunkedDocument,embedding:list[float]) -> EmbeddedTweetDocument:
        embedded_doc=EmbeddedTweetDocument(
            content=chunk.content,
            embedding=embedding,
            platform=chunk.platform,
            document_id=chunk.document_id,
            author_id=chunk.author_id,
            author_full_name=chunk.author_full_name,
            metadata=self.metadata,
            username=chunk.username,
            link=chunk.link,
            published_date=chunk.published_date
        )

        return embedded_doc