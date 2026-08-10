from zenml import pipeline

from pipelines.preference_dataset_generating_pipeline.steps.get_data_chunks import get_data_chunks
from pipelines.preference_dataset_generating_pipeline.steps.generate_preference_dataset import generate_preference_dataset
from pipelines.preference_dataset_generating_pipeline.steps.publish_dataset import publish_dataset


@pipeline
def preference_dataset_generating_pipeline(author_full_names:list[str]) -> str:
    chunks=get_data_chunks(author_full_names=author_full_names)
    preference_dataset=generate_preference_dataset(chunked_documents=chunks)
    last_step=publish_dataset(dataset=preference_dataset)

    return last_step.invocation_id