from data_preprocessors.data_embedders.base.data_embedder import DataEmbedder

from document_categories.vectordb_document_categories.chunked_documents.post_chunked_document import PostChunkedDocument
from document_categories.vectordb_document_categories.embedded_documents.embedded_post_document import EmbeddedPostDocument


class PostDataEmbedder(DataEmbedder):
    pre_embedding_cleaning=True

    def map_model(self,chunk:PostChunkedDocument,embedding:list[float]) -> EmbeddedPostDocument:
        embedded_doc=EmbeddedPostDocument(
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