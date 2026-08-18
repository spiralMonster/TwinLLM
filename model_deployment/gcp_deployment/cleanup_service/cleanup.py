from loguru import logger

from model_deployment.gcp_deployment.deployment.endpoint_manager import EndpointManager
from model_deployment.gcp_deployment.model_registration.model_registration import ModelRegistrar

from utils.exceptions.deployment_exceptions.gcp_exceptions.cleanup_exception import CleanupException
from settings import Settings


class CleanupService:
    def __init__(
            self,
            endpoint_manager:EndpointManager,
            model_registrar:ModelRegistrar
    ) -> None:

        self.endpoint_manager=endpoint_manager
        self.model_registrar=model_registrar


    def cleanup(self) -> None:
        try:
            logger.info("Cleaning up the GCP Resources.")

            logger.info(f"Deleting the Vertex AI Endpoint with display name: {Settings.GCP_ENDPOINT_NAME}")
            endpoint=self.endpoint_manager.get_endpoint()
            endpoint.delete(
                force=True,
                sync=True
            )
            logger.info("Successfully deleted the endpoint.")

            logger.info(f"Deleting the Model with display name: {Settings.DEPLOY_MODEL_ID.replace('/','--')}")
            model=self.model_registrar.get_model()
            model.delete(
                sync=True,
            )
            logger.info("Successfully deleted the model.")

            logger.info("Successfully cleaned up all the created GCP Resources. ")


        except Exception as e:
            logger.exception("Failed to cleanup the GCP resources.")
            raise CleanupException(
                "Failed cleaning up the created GCP Resources."
            ) from e





if __name__=="__main__":
    endpoint_mang=EndpointManager()
    model_reg=ModelRegistrar()

    cleanup_service=CleanupService(
        endpoint_manager=endpoint_mang,
        model_registrar=model_reg
    )

    cleanup_service.cleanup()
