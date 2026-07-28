from loguru import logger
from typing import Annotated
from zenml import step,get_step_context

from data_preprocessors.data_chunkers.dispatcher.chunking_dispatcher import ChunkingDispatcher
from data_preprocessors.data_embedders.dispatcher.embedding_dispatcher import EmbeddingDispatcher

from utils.batch_data import batch
from utils.exceptions.data_preprocessor_exceptions.data_embedding_exception import DataEmbeddingException

from pipelines.rag_feature_pipeline.metadata.get_chunks_metadata import get_chunk_metadata
from pipelines.rag_feature_pipeline.metadata.get_embedded_chunks_metadata import get_embedded_chunks_metadata


@step
def chunk_and_embed(
        cleaned_documents: Annotated[list,"cleaned_documents"]
) -> Annotated[list,"embedded_documents"]:

    chunked_docs=[]
    embedded_docs=[]

    for doc in cleaned_documents:
        chunks=ChunkingDispatcher.dispatch(cleaned_document=doc)

        if chunks:
            chunked_docs.extend(chunks)

            chunk_batches=batch(chunks,batch_size=10)
            for chunk_batch in chunk_batches:
                embedded_chunks=EmbeddingDispatcher.dispatch(chunked_documents=chunk_batch)
                if embedded_chunks:
                    embedded_docs.extend(embedded_chunks)


    if embedded_docs:
        metadata=dict()
        metadata["num_cleaned_documents"]=len(cleaned_documents)
        metadata["num_chunked_documents"]=len(chunked_docs)
        metadata["num_embedded_documents"]=len(embedded_docs)

        chunk_metadata=get_chunk_metadata(documents=chunked_docs)
        embedded_chunks_metadata=get_embedded_chunks_metadata(documents=embedded_docs)

        metadata["chunking"]=chunk_metadata
        metadata["embedding"]=embedded_chunks_metadata

        step_context=get_step_context()
        step_context.add_output_metadata(
            output_name="embedded_documents",
            metadata=metadata
        )

        return embedded_docs

    else:
        logger.error("Data Embedding operation failed. No embedded documents returned.")
        raise DataEmbeddingException("Failed to embedd the data.")






