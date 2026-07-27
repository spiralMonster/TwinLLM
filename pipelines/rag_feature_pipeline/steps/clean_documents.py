from loguru import logger
from typing import Annotated
from zenml import step,get_step_context

from data_preprocessors.data_cleaners.dispatcher.cleaning_dispatcher import CleaningDispatcher

from pipelines.rag_feature_pipeline.metadata.get_clean_documents_metadata import get_metadata

from utils.exceptions.data_preprocessor_exceptions.data_cleaning_exception import DataCleaningException


@step
def clean_documents(
        raw_documents: Annotated[list,"raw_documents"]
) -> Annotated[list,"cleaned_documents"]:

    cleaned_documents=[]
    for doc in raw_documents:
        cleaned_doc=CleaningDispatcher.dispatch(document=doc)
        if cleaned_doc:
            if isinstance(cleaned_doc,list):
                cleaned_documents.extend(cleaned_doc)

            else:
                cleaned_documents.append(cleaned_doc)


    if cleaned_documents:
        metadata=get_metadata(documents=cleaned_documents)

        step_context=get_step_context()
        step_context.add_output_metadata(
            output_name="cleaned_documents",
            metadata=metadata
        )

        return cleaned_documents


    else:
        logger.error("Data Cleaning operation failed. No cleaned documents returned.")
        raise DataCleaningException("Failed to clean the documents.")



