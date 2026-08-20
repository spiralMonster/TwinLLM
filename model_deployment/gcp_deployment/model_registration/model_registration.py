from loguru import logger
from google.cloud import aiplatform

from model_deployment.gcp_deployment.deployment.push_container_image import ContainerImagePusher
from model_deployment.gcp_deployment.deployment.upload_model import ModelUploader

from settings import Settings

from utils.exceptions.deployment_exceptions.gcp_exceptions.vertex_ai_exception import VertexAIException
from utils.exceptions.deployment_exceptions.gcp_exceptions.model_registration_exception import ModelRegisterationException
from utils.exceptions.deployment_exceptions.gcp_exceptions.model_not_found_exception import ModelNotFoundException
from utils.exceptions.deployment_exceptions.gcp_exceptions.many_model_found_exception import ManyModelFoundException



class ModelRegistrar:
    def __init__(
            self,
            container_image_pusher:ContainerImagePusher,
            model_uploader:ModelUploader
    ) -> None:
        aiplatform.init(
            project=Settings.GCP_PROJECT_ID,
            location=Settings.GCP_REGION
        )

        self.container_image_pusher=container_image_pusher
        self.model_uploader=model_uploader


    def register_model(self) -> aiplatform.Model:
        logger.info(f"Registering the Hugging Face Model : {Settings.DEPLOY_MODEL_ID} with GCP Vertex AI." )
        try:
            serving_container_image_uri=self.container_image_pusher.get_image_uri()
            _,artifact_uri=self.model_uploader.get_model_artifact_uri()

            model = aiplatform.Model.upload(
                display_name=Settings.DEPLOY_MODEL_ID.replace("/", "--"),
                serving_container_image_uri=serving_container_image_uri,
                artifact_uri=artifact_uri,
                serving_container_ports=[8080],
                serving_container_predict_route="/predict",
                serving_container_health_route="/health",
                serving_container_deployment_timeout=1800,
                serving_container_startup_probe_exec=[
                    "python3",
                    "-c",
                    (
                        "import urllib.request,sys; "
                        "sys.exit("
                        "0 if urllib.request.urlopen("
                        "'http://localhost:8080/health'"
                        ").getcode()==200 else 1"
                        ")"
                    ),
                ],
                serving_container_startup_probe_period_seconds=30,
                serving_container_startup_probe_timeout_seconds=10,
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








