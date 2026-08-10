import time
from loguru import logger
from typing import Annotated

from datasets import Dataset
from zenml import step,get_step_context

from dataset_generator.preference_dataset_generator.base.preference_dataset_generator import PreferenceDatasetGenerator
from dataset_generator.preference_dataset_generator.dispatcher.preference_dataset_gen_dispatcher import PreferenceDatasetGenDispatcher

from pipelines.preference_dataset_generating_pipeline.metadata.generate_preference_dataset_metadata import get_metadata

from document_categories.vectordb_document_categories.chunked_documents.base.chunked_document import ChunkedDocument
from document_categories.data_category import DataCategory

from utils.batch_data import batch
from utils.exceptions.model_exceptions.preference_dataset_generator_exception import PreferenceDatasetGeneratorException

from settings import Settings


@step
def generate_preference_dataset(
        chunked_documents:list[ChunkedDocument]
) -> Annotated[Dataset,"preference_dataset"]:

    preference_documents=[]

    grouped_documents=ChunkedDocument.group_by_class(chunked_documents)
    for document_class,documents in grouped_documents.items():
        document_category=document_class.get_category()
        if document_category==DataCategory.REPOSITORIES:
            documents=documents[:100]

        logger.info(f"{len(documents)} {document_category} Data Chunks retrieved successfully.")
        logger.info(f"Creating the Preference dataset from {document_category} data chunks.")

        num_docs_created=0
        batched_chunks=batch(documents,batch_size=30)
        for chunk_batch in batched_chunks:
            preference_docs=PreferenceDatasetGenDispatcher.dispatch(chunked_documents=chunk_batch)
            if preference_docs:
                num_docs_created+=len(preference_docs)
                preference_documents.extend(preference_docs)

            time.sleep(3)

        logger.info(f"{num_docs_created} Preference Triplets created successfully from {document_category} Data Chunks.")


    if preference_documents:
        instructions=[]
        chosen_answers=[]
        rejected_answers=[]

        for doc in preference_documents:
            instructions.append(doc.instruction)
            chosen_answers.append(doc.chosen_answer)
            rejected_answers.append(doc.rejected_answer)


        metadata=dict()
        metadata["model_settings"]={
            "temperature":Settings.TEMPERATURE_FOR_PREFERENCE_DATASET_GEN,
            "max_retries":Settings.MAX_RETRIES_FOR_PREFERENCE_DATASET_GEN,
            "llm_used":PreferenceDatasetGenerator.get_llm_models_used()
        }

        _metadata=get_metadata(documents=preference_documents)
        metadata["preference_dataset"]=_metadata

        step_context=get_step_context()
        step_context.add_output_metadata(
            output_name="preference_dataset",
            metadata=metadata
        )


        dataset=Dataset.from_dict(
            {
                "instructions":instructions,
                "chosen_answers":chosen_answers,
                "rejected_answers":rejected_answers
            }
        )

        logger.info(f"Successfully created {len(dataset)} Preference Triplets from the Data Chunks.")
        return dataset


    else:
        logger.info("No Preference Document Created...")
        raise PreferenceDatasetGeneratorException("Failed to generate Preference Dataset!!!")













