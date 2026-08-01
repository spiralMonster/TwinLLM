from zenml import pipeline

from pipelines.instruction_dataset_generating_pipeline.steps.get_data_chunks import get_data_chunks
from pipelines.instruction_dataset_generating_pipeline.steps.generate_instruction_dataset import generate_instruction_dataset
from pipelines.instruction_dataset_generating_pipeline.steps.publish_dataset_to_hugging_face_hub import publish_dataset_to_huggingface_hub


@pipeline
def instruct_dataset_generating_pipeline(author_full_names:list[str]) -> str:
    data_chunks=get_data_chunks(author_full_names=author_full_names)
    dataset=generate_instruction_dataset(chunked_documents=data_chunks)
    last_step=publish_dataset_to_huggingface_hub(dataset=dataset)

    return last_step.invocation_id