from loguru import logger
from typing import Annotated

from zenml import step,get_step_context

from document_categories.nosql_db_document_categories.base.user_document import UserDocument
from document_categories.vectordb_document_categories.chunked_documents.base.chunked_document import ChunkedDocument

from pipelines.instruction_dataset_generating_pipeline.utils.fetch_all_data_chunks import fetch_all_chunks
from pipelines.instruction_dataset_generating_pipeline.metadata.get_data_chunks_metadata import get_metadata

from utils.exceptions.qdrant_exceptions.find_document_exception import FindDocumentException


@step
def get_data_chunks(
        author_full_names:list[str]
) -> Annotated[list[ChunkedDocument],"chunked_documents"]:

    chunked_documents=[]
    for author_full_name in author_full_names:
        logger.info(f"Querying feature store to get data chunks for: {author_full_name}")

        full_name=author_full_name.split(" ")
        first_name=full_name[0]
        last_name=full_name[1]

        user=UserDocument.get_or_create(
            first_name=first_name,
            last_name=last_name
        )

        chunks=fetch_all_chunks(user=user)
        chunked_documents.extend(chunks)


    if chunked_documents:
        metadata=get_metadata(documents=chunked_documents)

        step_context=get_step_context()
        step_context.add_output_metadata(
            output_name="chunked_documents",
            metadata=metadata
        )

        return chunked_documents

    else:
        logger.info("Failed to retrieve Data Chunks from the Feature Store.")
        raise FindDocumentException("Failed to find the Chunked Documents.")



