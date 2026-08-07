from loguru import logger
from typing import Annotated

from datasets import load_dataset,Dataset
from zenml import step,get_step_context


@step
def load_datasets(
        dataset_id:Annotated[str,"dataset_id"]
) -> Annotated[tuple[Dataset,Dataset],"datasets"]:

    logger.info(f"Loading Dataset: {dataset_id} from Hugging Face.")
    dataset=load_dataset(dataset_id)["train"]

    len_dataset=len(dataset)
    ids=[_id for _id in range(len_dataset)]

    dataset=dataset.add_column("id",ids)

    metadata={
        "dataset_id":dataset_id,
        "number_of_instances_in_dataset":len_dataset
    }
    step_context=get_step_context()
    step_context.add_output_metadata(
        output_name="datasets",
        metadata=metadata
    )

    return dataset,dataset

