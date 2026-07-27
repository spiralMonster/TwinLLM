from loguru import logger
from typing import Annotated

from zenml import step,get_step_context

from document_categories.nosql_db_document_categories.base.base_document import Document
from document_categories.nosql_db_document_categories.base.user_document import UserDocument

from pipelines.rag_feature_pipeline.metadata.get_query_data_warehouse_metadata import get_metadata

from pipelines.rag_feature_pipeline.utils.fetch_all_data import fetch_all_data


@step
def query_data_warehouse(
        author_full_names:list[str]
) -> Annotated[list[Document],"raw_documents"]:

    documents=[]

    for author_full_name in author_full_names:
        logger.info(f"Querying data warehouse for User: {author_full_name}")

        author_full_name=author_full_name.split(" ")
        first_name=author_full_name[0]
        last_name=author_full_name[1]

        user=UserDocument.get_or_create(first_name=first_name,last_name=last_name)

        results=fetch_all_data(user=user)
        for key,value in results.items():
            for doc in value:
                documents.append(doc)


    metadata=get_metadata(documents=documents)

    step_context=get_step_context()
    step_context.add_output_metadata(
        output_name="raw_documents",
        metadata=metadata
    )

    logger.info("Successfully retrieved the documents from the Data warehouse.")

    return documents





