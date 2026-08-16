from loguru import logger

from document_categories.vectordb_document_categories.embedded_documents.base.embedded_document import EmbeddedDocument
from document_categories.rag_document_categories.query_document import Query

from rag.rag_steps.base.rag_step import RagStep
from models.cross_encoder_model import CrossEncoderModel


class Reranker(RagStep):
    model=CrossEncoderModel()

    def generate(self,query:Query,*args,**kwargs) -> list[EmbeddedDocument]:
        if "retrieved_documents" not in kwargs:
            logger.info("Need an argument 'retrieved_documents' to rerank the documents.")
            raise ValueError("Argument not found!!!")

        retrieved_documents=kwargs["retrieved_documents"]
        keep_top_k=kwargs.get("keep_top_k",5)

        if not (
            isinstance(retrieved_documents,list) and
            all(isinstance(doc,EmbeddedDocument) for doc in retrieved_documents)
        ):
            logger.info("Received an unexpected argument. The 'retrieved_documents' should be the list of EmbeddedDocuments.")
            raise ValueError("Unexpected argument received!!!")

        if isinstance(query,str):
            query=Query.from_str(content=query)

        if len(retrieved_documents)<=keep_top_k:
            logger.info("Reranked documents successfully.")
            return retrieved_documents

        else:
            query_content=query.content
            pairs=[
                (query_content,doc.content)
                for doc in retrieved_documents
            ]

            scores=self.model(pairs=pairs)

            score_doc=list(zip(scores,retrieved_documents))
            sorted_score_doc=sorted(score_doc,key=lambda x:x[0],reverse=True)

            reranked_docs=[doc for score,doc in sorted_score_doc[:keep_top_k]]
            reranked_docs=list(set(reranked_docs))

            logger.info("Reranked documents successfully.")
            return reranked_docs

