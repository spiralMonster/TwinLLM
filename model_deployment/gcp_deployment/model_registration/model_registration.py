from loguru import logger
from google.cloud import aiplatform

from settings import Settings

from utils.exceptions.deployment_exceptions.gcp_exceptions.vertex_ai_exception import VertexAIException
from utils.exceptions.deployment_exceptions.gcp_exceptions.model_registration_exception import ModelRegisterationException
from utils.exceptions.deployment_exceptions.gcp_exceptions.model_not_found_exception import ModelNotFoundException
from utils.exceptions.deployment_exceptions.gcp_exceptions.many_model_found_exception import ManyModelFoundException



class ModelRegistrar:
    def __init__(self) -> None:
        aiplatform.init(
            project=Settings.GCP_PROJECT_ID,
            location=Settings.GCP_REGION
        )


    @staticmethod
    def register_model() -> aiplatform.Model:
        logger.info(f"Registering the Hugging Face Model : {Settings.DEPLOY_MODEL_ID} with GCP Vertex AI." )
        try:
            model=aiplatform.Model.upload(
                display_name=Settings.DEPLOY_MODEL_ID.replace("/","--"),
                serving_container_image_uri=(
                    Settings.GCP_TGI_CONTAINER_URI
                ),
                serving_container_environment_variables={
                    "MODEL_ID":Settings.DEPLOY_MODEL_ID,
                    "HUGGING_FACE_HUB_TOKEN":Settings.HF_TOKEN,
                    "HF_HUB_ENABLE_HF_TRANSFER":"1",
                    "NUM_SHARD":"1"
                }
            )
            model.wait()

            logger.info("Hugging Face Model registered successfully with GCP Vertex AI.")

            return model

        except Exception as e:
            logger.info(f"Exception Encountered: {e}")
            raise ModelRegisterationException("Failed to register the Hugging Face Model with GCP Vertex AI.")


    @staticmethod
    def get_model() -> aiplatform.Model:
        try:
            display_name=Settings.DEPLOY_MODEL_ID.replace("/","--")
            logger.info(f"Fetching Vertex AI Model: {display_name}")

            models=aiplatform.Model.list(
                filter=f'display_name="{display_name}"'
            )

            if not models:
                logger.exception(f"Failed to find the Model: {display_name}")
                raise ModelNotFoundException(
                    f"Model: '{display_name}' was not found."
                )

            if len(models)>1:
                logger.exception(f"Found multiple Models with display name: '{display_name}'")
                raise ManyModelFoundException(
                    f"Multiple Models found with display name: {display_name}"
                )

            model=models[0]
            return model

        except Exception as e:
            logger.exception("Failed to fetch the model from the Vertex AI.")
            raise VertexAIException(
                "Failed to fetch Vertex AI Model."
            ) from e








