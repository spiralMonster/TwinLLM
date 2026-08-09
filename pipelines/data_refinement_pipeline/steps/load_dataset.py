from loguru import logger
from typing import Annotated

from datasets import load_dataset,Dataset
from zenml import step,get_step_context


@step
def load_datasets(
        dataset_id:Annotated[str,"dataset_id"]
) -> tuple[
    Annotated[Dataset,"evaluated_dataset"],
    Annotated[Dataset,"cleaned_dataset"]
]:

    logger.info(f"Loading Dataset: {dataset_id} from Hugging Face.")
    dataset=load_dataset(dataset_id)["train"]

    len_dataset=len(dataset)
    ids=[_id for _id in range(len_dataset)]

    dataset=dataset.add_column("id",ids)

    metadata_evaluated={
        "dataset_id":dataset_id,
        "dataset_type":"evaluated_dataset",
        "number_of_instances_in_dataset":len_dataset
    }
    step_context_evaluated=get_step_context()
    step_context_evaluated.add_output_metadata(
        output_name="evaluated_dataset",
        metadata=metadata_evaluated
    )
    
    metadata_cleaned ={
        "dataset_id":dataset_id,
        "dataset_type":"cleaned_dataset",
        "number_of_instances_in_dataset":len_dataset,
    }
    step_context_cleaned=get_step_context()
    step_context_cleaned.add_output_metadata(
        output_name="cleaned_dataset",
        metadata=metadata_cleaned
    )

    return dataset,dataset

