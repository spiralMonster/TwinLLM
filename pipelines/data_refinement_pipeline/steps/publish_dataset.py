from loguru import logger
from typing import Annotated

from datasets import Dataset
from huggingface_hub import login
from zenml import step,get_step_context

from utils.exceptions.model_exceptions.hugging_face_exception import HuggingFaceException
from settings import Settings


@step
def publish_dataset(
        dataset:Dataset,
        dataset_name:str,
        remark_about_dataset:str
) -> Annotated[str,"published_dataset"]:

    try:
        dataset=dataset.remove_columns(["id"])

        logger.info("Logging to Hugging Face Hub")
        hf_token=Settings.HF_TOKEN
        login(hf_token)

        hf_username=Settings.HF_USERNAME
        dataset_url=hf_username+"/"+dataset_name

        dataset.push_to_hub(dataset_url)
        logger.info(f"Successfully published dataset: {dataset_url} to Hugging Face Hub.")

        metadata=dict()
        metadata["dataset_name"]=dataset_name
        metadata["dataset_url"]=dataset_url
        metadata["remark"]=remark_about_dataset
        metadata["number_of_instances"]=len(dataset)
        metadata["dataset_features"]=list(dataset.features.keys())

        step_context=get_step_context()
        step_context.add_output_metadata(
            output_name="published_dataset",
            metadata=metadata
        )

        return remark_about_dataset
    
    except Exception as e:
        logger.info("Failed to push dataset to Hugging Face Hub")
        logger.info(f"Exception encountered: {e}")

        raise HuggingFaceException("Failed to upload dataset to Hugging Face.")