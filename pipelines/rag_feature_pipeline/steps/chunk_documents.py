from loguru import logger
from typing import Annotated
from zenml import step,get_step_context

from data_preprocessors.data_chunkers.dispatcher.chunking_dispatcher import ChunkingDispatcher

from pipelines.rag_feature_pipeline.metadata.get_chunks_metadata import get_metadata

from utils.exceptions.data_preprocessor_exceptions.data_chunking_exception import DataChunkingException


@step
def chunk_documents(
        cleaned_documents:Annotated[list,"cleaned_documents"]
) -> Annotated[list,"chunked_documents"]:

    chunked_docs=[]
    for doc in cleaned_documents:
        chunks=ChunkingDispatcher.dispatch(cleaned_document=doc)
        if chunks:
            chunked_docs.extend(chunks)



    if chunked_docs:
        metadata=dict()
        metadata["num_cleaned_documents"]=len(cleaned_documents)
        metadata["num_chunked_documents"]=len(chunked_docs)

        chunk_metadata=get_metadata(documents=chunked_docs)
        for key,value in chunk_metadata.items():
            metadata[key]=value


        step_context=get_step_context()
        step_context.add_output_metadata(
            output_name="chunked_documents",
            metadata=metadata
        )

        return chunked_docs

    else:
        logger.error("Data Chunking operation failed. No chunked documents returned.")
        raise DataChunkingException("Failed to chunk the data.")


