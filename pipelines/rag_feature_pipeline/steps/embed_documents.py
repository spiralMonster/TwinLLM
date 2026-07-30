from loguru import logger
from typing import Annotated
from zenml import step,get_step_context

from document_categories.vectordb_document_categories.base.vector_base_document import VectorBaseDocument

from data_preprocessors.data_embedders.dispatcher.embedding_dispatcher import EmbeddingDispatcher

from utils.batch_data import batch
from utils.exceptions.data_preprocessor_exceptions.data_embedding_exception import DataEmbeddingException

from pipelines.rag_feature_pipeline.metadata.get_embedded_chunks_metadata import get_metadata


@step
def embed_documents(
        chunked_documents:Annotated[list,"chunked_documents"]
) -> Annotated[list,"embedded_documents"]:

    embedded_docs=[]
    grouped_documents=VectorBaseDocument.group_by_class(chunked_documents)
    for document_class,docs in grouped_documents.items():
        collection_name=document_class.get_collection_name()
        logger.info(f"Embedding {collection_name} documents.")

        doc_batches=batch(docs,batch_size=10)
        for doc_batch in doc_batches:
            embedded_batch=EmbeddingDispatcher.dispatch(chunked_documents=doc_batch)
            if embedded_batch:
                embedded_docs.extend(embedded_batch)

    if embedded_docs:
        metadata=dict()
        metadata["num_chunked_documents"]=len(chunked_documents)
        metadata["num_embedded_documents"]=len(embedded_docs)

        embed_metadata=get_metadata(documents=embedded_docs)
        for key,value in embed_metadata.items():
            metadata[key]=value


        step_context=get_step_context()
        step_context.add_output_metadata(
            output_name="embedded_documents",
            metadata=metadata
        )

        return embedded_docs


    else:
        logger.error("Data Embedding operation failed. No embedded documents returned.")
        raise DataEmbeddingException("Failed to embedd the data.")
