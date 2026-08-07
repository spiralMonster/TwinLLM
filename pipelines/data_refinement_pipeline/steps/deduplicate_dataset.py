from loguru import logger
from typing import Annotated

from datasets import Dataset
from zenml import step,get_step_context

from data_refinement.data_deduplication.exact_deduplication import exact_deduplication
from data_refinement.data_deduplication.fuzzy_deduplication import min_hash_deduplication
from data_refinement.data_deduplication.semantic_deduplication import semantic_deduplication

from pipelines.data_refinement_pipeline.metadata.get_deduplicate_dataset_metadata import get_metadata

from settings import Settings

@step
def deduplicate_dataset(
        cleaned_dataset:Dataset
) -> Annotated[Dataset,"deduplicated_dataset"]:

    logger.info("Data Deduplication Started.")

    metadata=dict()
    metadata["num_instances_before_deduplication"]=len(cleaned_dataset)
    metadata["num_instances_after_deduplication"]=len(cleaned_dataset)
    metadata["num_instances_deduplicated"]=0

    logger.info("Exact Deduplication of Dataset...")
    instruction_key=Settings.INSTRUCTION_KEY
    output_key=Settings.OUTPUT_KEY

    cleaned_dataset,deduplicating_metadata=exact_deduplication(
        dataset=cleaned_dataset,
        instruction_key=instruction_key,
        output_key=output_key
    )

    metadata["exact_deduplication"]=get_metadata(
        deduplicating_metadata=deduplicating_metadata,
        additional_metadata_key=None,
        additional_metadata=None
    )


    logger.info("Fuzzy Deduplication Using MIN-HASH Algorithm...")
    fuzzy_deduplication_arguments=Settings.FUZZY_DEDUPLICATION_ARGUMENTS

    cleaned_dataset,deduplicating_metadata=min_hash_deduplication(
        dataset=cleaned_dataset,
        instruction_key=instruction_key,
        output_key=output_key,
        shingle_length=fuzzy_deduplication_arguments["shingle_length"],
        number_of_hashes_per_document=fuzzy_deduplication_arguments["number_of_hashes_per_document"],
        minimum_similarity_threshold=fuzzy_deduplication_arguments["minimimum_similarity_threshold"]
    )

    metadata["fuzzy_deduplication"]=get_metadata(
        deduplicating_metadata=deduplicating_metadata,
        additional_metadata_key="algorithm_details",
        additional_metadata=fuzzy_deduplication_arguments
    )


    logger.info("Semantic Deduplication of Dataset...")
    semantic_deduplication_arguments=Settings.SEMANTIC_DEDUPLICATION_ARGUMENTS
    
    cleaned_dataset,deduplicating_metadata=semantic_deduplication(
        dataset=cleaned_dataset,
        instruction_key=instruction_key,
        output_key=output_key,
        minimum_cosine_similarity_threshold=semantic_deduplication_arguments["minimum_cosine_similarity_threshold"]
    )
    
    metadata["semantic_deduplication"]=get_metadata(
        deduplicating_metadata=deduplicating_metadata,
        additional_metadata_key="algorithm_details",
        additional_metadata=semantic_deduplication_arguments
    )
    
    logger.info("Data Deduplication Completed.")
    metadata["num_instances_after_deduplication"]=len(cleaned_dataset)
    metadata["num_instances_deduplicated"]=metadata["num_instances_before_deduplication"]- metadata["num_instances_after_deduplication"]


    step_context=get_step_context()
    step_context.add_output_metadata(
        output_name="deduplicated_dataset",
        metadata=metadata
    )

    return cleaned_dataset

