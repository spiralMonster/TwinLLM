from data_preprocessors.data_embedders.base.data_embedder import DataEmbedder, ChunkedDocumentT, EmbeddedDocumentT

from document_categories.vectordb_document_categories.chunked_documents.article_chunked_document import ArticleChunkedDocument
from document_categories.vectordb_document_categories.embedded_documents.embedded_article_document import EmbeddedArticleDocument


class ArticleDataEmbedder(DataEmbedder):
    def map_model(self,chunk:ArticleChunkedDocument,embedding:list[float]) -> EmbeddedArticleDocument:
        embedded_doc=EmbeddedArticleDocument(
            content=chunk.content,
            embedding=embedding,
            platform=chunk.platform,
            document_id=chunk.document_id,
            author_id=chunk.author_id,
            author_full_name=chunk.author_full_name,
            metadata=self.metadata,
            username=chunk.username,
            link=chunk.link,
            title=chunk.title,
            description=chunk.description,
            published_date=chunk.published_date
        )

        return embedded_doc