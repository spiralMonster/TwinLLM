from abc import abstractmethod,ABC
from typing import Generic,TypeVar,cast

from document_categories.vectordb_document_categories.chunked_documents.base.chunked_document import ChunkedDocument
from document_categories.vectordb_document_categories.embedded_documents.base.embedded_document import EmbeddedDocument

from models.embedding_model import EmbeddingModel

ChunkedDocumentT=TypeVar("ChunkedDocumentT",bound=ChunkedDocument)
EmbeddedDocumentT=TypeVar("EmbeddedDocumentT",bound=EmbeddedDocument)

embedding_model=EmbeddingModel()


class DataEmbedder(ABC,Generic[ChunkedDocumentT,EmbeddedDocumentT]):
    @property
    def metadata(self) -> dict:
        _metadata={
            "embedding_model_id":embedding_model.model_id,
            "embedding_size":embedding_model.embedding_size,
            "max_input_lenght":embedding_model.max_input_length
        }

        return _metadata


    @abstractmethod
    def map_model(self,chunk:ChunkedDocumentT,embedding:list[float]) -> EmbeddedDocumentT:
        pass


    def embed_batch(self,chunked_data:list[ChunkedDocumentT]) -> list[EmbeddedDocumentT]:
        embedding_model_input=[data.content for data in chunked_data]

        embeddings=embedding_model(
            input_text=embedding_model_input,
            to_list=True
        )
        final_embeddings=[
            cast(list[float],embed)
            for embed in embeddings
        ]

        result=[
            self.map_model(chunk=chunk,embedding=embedding)
            for chunk,embedding in zip(chunked_data,final_embeddings)
        ]

        return result



    def embed(self,chunk:ChunkedDocumentT) -> EmbeddedDocumentT:
        embed_data=self.embed_batch(
            chunked_data=[chunk]
        )[0]

        return embed_data
