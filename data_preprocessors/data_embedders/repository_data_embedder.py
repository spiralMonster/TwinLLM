from data_preprocessors.data_embedders.base.data_embedder import DataEmbedder

from document_categories.vectordb_document_categories.chunked_documents.repository_chunked_document import RepositoryChunkedDocument
from document_categories.vectordb_document_categories.embedded_documents.embedded_repository_document import EmbeddedRepositoryDocument


class RepositoryDataEmbedder(DataEmbedder):
    pre_embedding_cleaning=False

    def map_model(self,chunk:RepositoryChunkedDocument,embedding:list[float]) -> EmbeddedRepositoryDocument:
        embedded_doc=EmbeddedRepositoryDocument(
            content=chunk.content,
            embedding=embedding,
            platform=chunk.platform,
            document_id=chunk.document_id,
            author_id=chunk.author_id,
            author_full_name=chunk.author_full_name,
            metadata=self.metadata,
            repository_name=chunk.repository_name,
            link=chunk.link,
            file_name=chunk.file_name,
            programming_language_used=chunk.programming_language_used
        )

        return embedded_doc