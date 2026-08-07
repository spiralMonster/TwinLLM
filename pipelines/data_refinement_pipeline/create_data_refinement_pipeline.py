from zenml import pipeline

from pipelines.data_refinement_pipeline.steps.load_dataset import load_datasets
from pipelines.data_refinement_pipeline.steps.filter_dataset import filter_dataset
from pipelines.data_refinement_pipeline.steps.deduplicate_dataset import deduplicate_dataset
from pipelines.data_refinement_pipeline.steps.data_quality_evaluation import data_quality_evaluation
from pipelines.data_refinement_pipeline.steps.publish_dataset import publish_dataset

from settings import Settings


@pipeline
def data_refinement_pipeline(instruct_dataset_id:str) -> list[str]:
    evaluated_dataset,cleaned_dataset=load_datasets(dataset_id=instruct_dataset_id)

    evaluated_dataset,cleaned_dataset=filter_dataset(
        evaluated_dataset=evaluated_dataset,
        cleaned_dataset=cleaned_dataset
    )

    cleaned_dataset=deduplicate_dataset(cleaned_dataset=cleaned_dataset)

    evaluated_dataset,cleaned_dataset=data_quality_evaluation(
        evaluated_dataset=evaluated_dataset,
        cleaned_dataset=cleaned_dataset
    )

    evaluated_dataset_name=Settings.EVALUATED_INSTRUCT_DATASET_NAME
    cleaned_dataset_name=Settings.CLEANED_INSTRUCT_DATASET_NAME

    last_step1=publish_dataset(
        dataset=evaluated_dataset,
        dataset_name=evaluated_dataset_name,
        remark_about_dataset="The instruct dataset evaluated on various factors."
    )

    last_step2=publish_dataset(
        dataset=cleaned_dataset,
        dataset_name=cleaned_dataset_name,
        remark_about_dataset="The cleaned instruct dataset."
    )

    return [last_step1.invocation_id,last_step2.invocation_id]