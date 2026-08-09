from loguru import logger
from typing import Annotated

from datasets import Dataset
from zenml import step,get_step_context

from data_refinement.data_quality_evaluation.using_llm_as_judge.data_quality_based_evaluation_and_filtering import quality_based_evaluation_and_filtering

from pipelines.data_refinement_pipeline.metadata.get_data_quality_evaluation_metadata import get_metadata

from settings import  Settings


@step
def data_quality_evaluation(
        evaluated_dataset:Dataset,
        cleaned_dataset:Dataset
) -> tuple[
    Annotated[Dataset,"evaluated_dataset_after_data_quality_evaluation"],
    Annotated[Dataset,"cleaned_dataset_after_data_quality_evaluation"]
]:

    logger.info("Data Quality Evaluation and Filtering using LLM AS JUGDE")

    num_instances_before_filtering=len(cleaned_dataset)
    instruction_key=Settings.INSTRUCTION_KEY
    output_key=Settings.OUTPUT_KEY

    filters={
        "minimum_score":Settings.DATA_QUALITY_MINIMUM_SCORE_THRESHOLD
    }
    evaluated_dataset,cleaned_dataset=quality_based_evaluation_and_filtering(
        evaluated_dataset=evaluated_dataset,
        cleaned_dataset=cleaned_dataset,
        instruction_key=instruction_key,
        output_key=output_key,
        filters=filters,
        create_evaluation_dataset=True,
        filter_dataset=True
    )

    scores=list(evaluated_dataset["Score_given_by_LLM_AS_JUDGE"])
    mean_score=sum(scores)//len(evaluated_dataset)

    num_instances_after_filtering=len(cleaned_dataset)

    metadata=get_metadata(
        num_instances_before_filtering=num_instances_before_filtering,
        num_instances_after_filtering=num_instances_after_filtering,
        mean_evaluation_score_given_by_llm_as_judge=mean_score
    )
    
    metadata_cleaned=metadata
    step_context_cleaned=get_step_context()
    step_context_cleaned.add_output_metadata(
        output_name="cleaned_dataset_after_data_quality_evaluation",
        metadata=metadata_cleaned
    )

    metadata_evaluated=dict()
    metadata_evaluated["num_instances"]=(len(evaluated_dataset),)
    metadata_evaluated["dataset_features"]=list(evaluated_dataset.features.keys())
    step_context_evaluated=get_step_context()
    step_context_evaluated.add_output_metadata(
        output_name="evaluated_dataset_after_data_quality_evaluation",
        metadata=metadata_evaluated
    )

    logger.info("Data Quality Evaluated And Filtered.")

    return evaluated_dataset,cleaned_dataset