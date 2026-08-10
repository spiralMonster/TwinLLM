from loguru import logger
from typing import Annotated

from datasets import Dataset
from huggingface_hub import login
from zenml import step,get_step_context

from settings import Settings
from utils.exceptions.model_exceptions.hugging_face_exception import HuggingFaceException


@step
def publish_dataset(
        dataset:Dataset
) -> Annotated[str,"published_dataset"]:

    logger.info("Logging into Hugging Face Hub.")
    try:
        hf_token=Settings.HF_TOKEN
        login(hf_token)

        hf_username=Settings.HF_USERNAME
        dataset_name=Settings.PREFERENCE_DATASET_NAME
        dataset_id=hf_username+"/"+dataset_name

        dataset.push_to_hub(dataset_id)
        logger.info(f"Dataset successfully uploaded to: {dataset_id}")

        message="Preference Dataset published successfully to Hugging Face Hub."

        metadata=dict()
        metadata["dataset_name"]=dataset_name
        metadata["dataset_id"]=dataset_id
        metadata["remark"]="Preference Dataset consisting of the triples of instruction,chosen answer and rejected answer."
        metadata["dataset_features"]=dataset.features.keys()
        metadata["number_of_instances"]=len(dataset)

        step_context=get_step_context()
        step_context.add_output_metadata(
            output_name="published_dataset",
            metadata=metadata
        )

        return message

    except Exception as e:
        logger.info("Failed to push dataset to Hugging Face Hub")
        logger.info(f"Exception encountered: {e}")

        raise HuggingFaceException("Failed to upload dataset to Hugging Face.")


