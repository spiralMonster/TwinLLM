from loguru import logger
from typing import Annotated,Any

from zenml import step,get_step_context

from document_categories.vectordb_document_categories.base.vector_base_document import VectorBaseDocument

from utils.batch_data import batch
from utils.exceptions.qdrant_exceptions.document_insertion_exception import DocumentInsertionException


@step
def load_to_vector_db(
        documents: Annotated[list,"documents"]
) -> Annotated[str,"load_to_vector_db"]:
    num_documents=len(documents)
    logger.info(f"Loading {num_documents} into the vector database.")

    num_docs_loaded_successfully=0
    batch_size=4

    metadata=dict()
    metadata["num_documents_received "]=num_documents
    metadata["num_documents_loaded_successfully"]=num_docs_loaded_successfully

    grouped_docs=VectorBaseDocument.group_by_class(documents)
    for document_class,docs in grouped_docs.items():
        collection_name=document_class.get_collection_name()
        doc_loaded_in_collection_successfully=0
        logger.info(f"Loading documents into {collection_name}")

        metadata[collection_name]=dict()
        metadata[collection_name]["num_documents_received "]=len(docs)
        metadata[collection_name]["num_documents_loaded_successfully"]=doc_loaded_in_collection_successfully

        doc_batches=batch(docs,batch_size=batch_size)
        for doc_batch in doc_batches:
            try:
                document_class.bulk_insert(documents=doc_batch)
                doc_loaded_in_collection_successfully+=len(doc_batch)

            except Exception as e:
                logger.info(f"Exception encountered: {e}")
                continue

        metadata[collection_name]["num_documents_loaded_successfully"]=doc_loaded_in_collection_successfully
        num_docs_loaded_successfully+=doc_loaded_in_collection_successfully


    metadata["num_documents_loaded_successfully"]=num_docs_loaded_successfully

    if num_docs_loaded_successfully:

        step_context=get_step_context()
        step_context.add_output_metadata(
            output_name="load_to_vector_db",
            metadata=metadata
        )

        return "Documents loaded successfully in Vector database."



    else:
        logger.info("Failed to insert any document in vector database.")
        raise DocumentInsertionException("Failed to insert document.")



