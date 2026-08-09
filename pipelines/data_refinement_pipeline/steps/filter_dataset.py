from loguru import logger
from typing import Annotated

from datasets import Dataset
from zenml import step,get_step_context

from data_refinement.rule_based_evaluation_and_filtering.length_based_evaluation_and_filtering import length_based_evaluation_and_filtering
from data_refinement.rule_based_evaluation_and_filtering.toxicity_based_evaluation_and_filtering import toxicity_based_evaluation_and_filtering
from data_refinement.rule_based_evaluation_and_filtering.format_based_evaluation_and_filtering import format_based_evaluation_and_filtering

from pipelines.data_refinement_pipeline.metadata.get_filter_dataset_metadata import get_metadata

from settings import Settings


@step
def filter_dataset(
        evaluated_dataset:Dataset,
        cleaned_dataset:Dataset,
) -> tuple[
    Annotated[Dataset,"evaluated_dataset_after_filtering"],
    Annotated[Dataset,"cleaned_dataset_after_filtering"]
]:

    metadata=dict()
    metadata["num_instances_before_filtering"]=len(cleaned_dataset)
    metadata["num_instances_after_filtering"]=len(cleaned_dataset)
    metadata["num_instances_filtered"]=0
    
    logger.info("Dataset Filtering Started.")
    logger.info("Filtering Dataset based on the length of the content.")
    
    instruction_key=Settings.INSTRUCTION_KEY
    output_key=Settings.OUTPUT_KEY
    instruction_length_based_filters=Settings.INSTRUCTION_LENGTH_BASED_FILTERS
    output_length_based_filters=Settings.OUTPUT_LENGTH_BASED_FILTERS

    (evaluated_dataset,cleaned_dataset),filtering_metadata=length_based_evaluation_and_filtering(
        evaluated_dataset=evaluated_dataset,
        cleaned_dataset=cleaned_dataset,
        instruction_key=instruction_key,
        output_key=output_key,
        instruction_filters=instruction_length_based_filters,
        output_filters=output_length_based_filters,
        create_evaluation_dataset=True,
        filter_dataset=True
    )
    
    metadata["length_based_filtering"]=get_metadata(
        filtering_metadata=filtering_metadata,
        instruction_filters=instruction_length_based_filters,
        output_filters=output_length_based_filters
    )
    
    
    logger.info("Filtering dataset based on the toxicity of the content.")
    
    instruction_toxicity_based_filters=Settings.INSTRUCTION_TOXICITY_BASED_FILTERS
    output_toxicity_based_filters=Settings.OUTPUT_TOXICITY_BASED_FILTERS

    (evaluated_dataset,cleaned_dataset),filtering_metadata=toxicity_based_evaluation_and_filtering(
        evaluated_dataset=evaluated_dataset,
        cleaned_dataset=cleaned_dataset,
        instruction_key=instruction_key,
        output_key=output_key,
        instruction_filters=instruction_toxicity_based_filters,
        output_filters=output_toxicity_based_filters,
        create_evaluation_dataset=True,
        filter_dataset=True
    )
    
    metadata["toxicity_based_filtering"]=get_metadata(
        filtering_metadata=filtering_metadata,
        instruction_filters=instruction_toxicity_based_filters,
        output_filters=output_toxicity_based_filters
    )
    
    
    logger.info("Filtering the dataset based on the format of the content.")
    
    instruction_format_based_filters=Settings.INSTRUCTION_FORMAT_BASED_FILTERS
    output_format_based_filters=Settings.OUTPUT_FORMAT_BASED_FILTERS

    (evaluated_dataset,cleaned_dataset),filtering_metadata=format_based_evaluation_and_filtering(
        evaluated_dataset=evaluated_dataset,
        cleaned_dataset=cleaned_dataset,
        instruction_key=instruction_key,
        output_key=output_key,
        instruction_filters=instruction_format_based_filters,
        output_filters=output_format_based_filters,
        create_evaluation_dataset=True,
        filter_dataset=True
    )
    
    metadata["format_based_filtering"]=get_metadata(
        filtering_metadata=filtering_metadata,
        instruction_filters=instruction_format_based_filters,
        output_filters=output_format_based_filters
    )

    metadata["num_instances_after_filtering"]=len(cleaned_dataset)
    metadata["num_instances_filtered"]=metadata["num_instances_before_filtering"]-metadata["num_instances_after_filtering"]
    logger.info("Dataset Filtering Completed.")

    metadata_cleaned=metadata
    step_context_cleaned=get_step_context()
    step_context_cleaned.add_output_metadata(
        output_name="cleaned_dataset_after_filtering",
        metadata=metadata_cleaned
    )

    metadata_evaluated=dict()
    metadata_evaluated["num_instances"]=len(evaluated_dataset),
    metadata_evaluated["dataset_features"]=list(evaluated_dataset.features.keys())
    step_context_evaluated=get_step_context()
    step_context_evaluated.add_output_metadata(
        output_name="evaluated_dataset_after_filtering",
        metadata=metadata_evaluated
    )


    
    return evaluated_dataset,cleaned_dataset

