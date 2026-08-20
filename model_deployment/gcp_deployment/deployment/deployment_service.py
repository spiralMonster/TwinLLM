from loguru import logger
from google.cloud import aiplatform

from model_deployment.gcp_deployment.infrastructure.infrastructure_validator import InfrastructureValidator
from model_deployment.gcp_deployment.deployment.push_container_image import ContainerImagePusher
from model_deployment.gcp_deployment.deployment.upload_model import ModelUploader
from model_deployment.gcp_deployment.model_registration.model_registration import ModelRegistrar
from model_deployment.gcp_deployment.deployment.endpoint_manager import EndpointManager
from model_deployment.gcp_deployment.cleanup_service.cleanup import CleanupService

from settings import Settings
from utils.exceptions.deployment_exceptions.gcp_exceptions.availability_exception import AvailabilityException
from utils.exceptions.deployment_exceptions.gcp_exceptions.model_deployment_exception import ModelDeploymentException


class DeploymentService:
    def __init__(
            self,
            infrastructure_validator:InfrastructureValidator,
            container_image_pusher:ContainerImagePusher,
            model_uploader:ModelUploader,
            model_registrar:ModelRegistrar,
            endpoint_manager:EndpointManager
    ) -> None:

        self.infrastructure_validator=infrastructure_validator
        self.container_image_pusher=container_image_pusher
        self.model_uploader=model_uploader
        self.model_registrar=model_registrar
        self.endpoint_manager=endpoint_manager


    def prepare_artifacts(self) -> None:
        self.container_image_pusher.push_image()
        self.model_uploader.upload_model()


    def deploy(self) -> aiplatform.Endpoint:
        logger.info("Deploying Model to GCP Vertex AI.")

        if self.infrastructure_validator.check_quotas() and self.infrastructure_validator.check_gpu():
            try:
                self.prepare_artifacts()

                endpoint = self.endpoint_manager.create_endpoint()
                model = self.model_registrar.register_model()
                deployed_endpoint=model.deploy(
                    endpoint=endpoint,
                    machine_type=Settings.GCP_MACHINE_TYPE,
                    accelerator_type=Settings.GCP_ACCELERATOR_TYPE,
                    accelerator_count=Settings.GCP_ACCELERATOR_COUNT,
                    min_replica_count=Settings.GCP_MIN_REPLICA_COUNT,
                    max_replica_count=Settings.GCP_MAX_REPLICA_COUNT,
                    sync=True
                )

                logger.info(f"Model successfully deployed to GCP Vertex AI on endpoint: {deployed_endpoint.resource_name}")
                return deployed_endpoint

            except Exception as e:
                logger.info("Failed to deploy model to GCP Vertex AI.")
                logger.info("Initiating the Cleanup Service.")

                cleanup_service=CleanupService(
                    container_image_pusher=self.container_image_pusher,
                    model_uploader=self.model_uploader,
                    endpoint_manager=self.endpoint_manager,
                    model_registrar=self.model_registrar
                )

                try:
                    cleanup_service.cleanup()

                except Exception as e:
                    logger.info(f"Exception encountered: {e}")
                    logger.info(
                        "Failed to delete some GCP resources."
                        "Please delete those resources manually."
                    )


                raise ModelDeploymentException("Failed to deploy model to GCP Vertex AI.") from e


        else:
            logger.info("Requested Infrastructure Not Available")
            logger.info("Deployment Failed.")

            raise AvailabilityException("Deployment Failed due to Infrastructure Availability.")




if __name__=="__main__":
    infrastructure_val=InfrastructureValidator()
    img_pusher=ContainerImagePusher()
    model_upl=ModelUploader()
    model_reg=ModelRegistrar(
        container_image_pusher=img_pusher,
        model_uploader=model_upl
    )
    endpoint_mang=EndpointManager()

    deployment_service=DeploymentService(
        infrastructure_validator=infrastructure_val,
        container_image_pusher=img_pusher,
        model_uploader=model_upl,
        model_registrar=model_reg,
        endpoint_manager=endpoint_mang
    )

    deployment_service.deploy()