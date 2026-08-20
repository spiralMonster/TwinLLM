from loguru import logger

from google.api_core.exceptions import NotFound

from model_deployment.gcp_deployment.deployment.push_container_image import ContainerImagePusher
from model_deployment.gcp_deployment.deployment.upload_model import ModelUploader
from model_deployment.gcp_deployment.deployment.endpoint_manager import EndpointManager
from model_deployment.gcp_deployment.model_registration.model_registration import ModelRegistrar

from utils.exceptions.deployment_exceptions.gcp_exceptions.cleanup_exception import CleanupException
from settings import Settings


class CleanupService:
    def __init__(
            self,
            container_image_pusher:ContainerImagePusher,
            model_uploader:ModelUploader,
            endpoint_manager:EndpointManager,
            model_registrar:ModelRegistrar
    ) -> None:

        self.container_image_pusher=container_image_pusher
        self.model_uploader=model_uploader
        self.endpoint_manager=endpoint_manager
        self.model_registrar=model_registrar



    def cleanup(self) -> None:
        try:
            logger.info("Cleaning up the GCP Resources.")

            logger.info(f"Deleting the Vertex AI Endpoint with display name: {Settings.GCP_ENDPOINT_NAME}")
            endpoint=self.endpoint_manager.get_endpoint()
            try:
                endpoint.delete(
                    force=True,
                    sync=True
                )
                logger.info("Successfully deleted the endpoint.")
            
            except NotFound:
                logger.info(
                    f"The endpoint does not exists: {endpoint.name}"
                    "Nothing to clean"
                )

            except Exception as e:
                logger.info(f"Exception encountered: {e}")
                logger.info(
                    f"Failed to delete the Endpoint: {endpoint.name}",
                    "Please do it manually."
                )

            logger.info(f"Deleting the Model with display name: {Settings.DEPLOY_MODEL_ID.replace('/','--')}")
            model=self.model_registrar.get_model()
            try:
                model.delete(
                    sync=True,
                )
                logger.info("Successfully deleted the model.")

            except NotFound:
                logger.info(
                    f"The Model: {model.name} does not exists."
                    "Nothing to clean"
                )

            except Exception as e:
                logger.info(f"Exception encountered: {e}")
                logger.info(
                    f"Failed to delete the Model: {model.name}"
                    "Please do it manually."
                )



            self.container_image_pusher.delete_repository()
            self.model_uploader.delete_model_artifacts()

            logger.info("Successfully cleaned up all the created GCP Resources. ")


        except Exception as e:
            logger.exception("Failed to cleanup the GCP resources.")
            raise CleanupException(
                "Failed cleaning up the created GCP Resources."
            ) from e





if __name__=="__main__":
    img_push=ContainerImagePusher()
    model_upl=ModelUploader()
    endpoint_mang=EndpointManager()
    model_reg=ModelRegistrar(
        container_image_pusher=img_push,
        model_uploader=model_upl
    )


    cleanup_service=CleanupService(
        container_image_pusher=img_push,
        model_uploader=model_upl,
        endpoint_manager=endpoint_mang,
        model_registrar=model_reg
    )

    cleanup_service.cleanup()
