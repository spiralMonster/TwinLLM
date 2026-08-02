from loguru import logger
from typing import Annotated
from zenml import step,get_step_context

from datasets import Dataset
from huggingface_hub import login

from settings import Settings
from utils.exceptions.model_exceptions.hugging_face_exception import HuggingFaceException

@step
def publish_dataset_to_huggingface_hub(
        dataset:Annotated[Dataset,"instruction_dataset"]
) -> Annotated[str,"publish_datset_to_hub"]:

    logger.info("Logging into Hugging Face Hub.")
    try:
        hf_token=Settings.HF_TOKEN
        login(hf_token)

        hf_username=Settings.HF_USERNAME
        dataset_name=Settings.INSTRUCT_DATASET_NAME
        dataset_url=hf_username+"/"+dataset_name

        dataset.push_to_hub(dataset_url)
        logger.info(f"Dataset successfully uploaded to: {dataset_url}")

        message="Dataset pushed successfully to Hugging Face Hub."

        metadata=dict()
        metadata["dataset_name"]=dataset_name
        metadata["dataset_url"]=dataset_url
        metadata["number_of_data_instances"]=len(dataset)

        step_context=get_step_context()
        step_context.add_output_metadata(
            output_name="publish_datset_to_hub",
            metadata=metadata
        )

        return message

    except Exception as e:
        logger.info("Failed to push dataset to Hugging Face Hub")
        logger.info(f"Exception encountered: {e}")

        raise HuggingFaceException("Failed to upload dataset to Hugging Face.")
