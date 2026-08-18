from loguru import logger
from google.cloud import aiplatform

from model_deployment.gcp_deployment.infrastructure.infrastructure_validator import InfrastructureValidator
from model_deployment.gcp_deployment.model_registration.model_registration import ModelRegistrar
from model_deployment.gcp_deployment.deployment.endpoint_manager import EndpointManager

from settings import Settings
from utils.exceptions.deployment_exceptions.gcp_exceptions.availability_exception import AvailabilityException
from utils.exceptions.deployment_exceptions.gcp_exceptions.model_deployment_exception import ModelDeploymentException


class DeploymentService:
    def __init__(
            self,
            infrastructure_validator:InfrastructureValidator,
            model_registrar:ModelRegistrar,
            endpoint_manager:EndpointManager
    ) -> None:

        self.infrastructure_validator=infrastructure_validator
        self.model_registrar=model_registrar
        self.endpoint_manager=endpoint_manager


    def deploy(self) -> aiplatform.Endpoint:
        logger.info("Deploying Model to GCP Vertex AI.")

        if self.infrastructure_validator.check_quotas() and self.infrastructure_validator.check_gpu():
            endpoint = self.endpoint_manager.create_endpoint()
            model = self.model_registrar.register_model()

            try:
                deployed_endpoint=model.deploy(
                    endpoint=endpoint,
                    machine_type=Settings.GCP_MACHINE_TYPE,
                    accelerator_type=Settings.GCP_ACCELERATOR_TYPE,
                    accelerator_count=Settings.GCP_ACCELERATOR_COUNT,
                    min_replica_count=Settings.GCP_MIN_REPLICA_COUNT,
                    max_replica_count=Settings.GCP_MAX_REPLICA_COUNT
                )

                logger.info(f"Model successfully deployed to GCP Vertex AI on endpoint: {deployed_endpoint.resource_name}")
                return deployed_endpoint

            except Exception as e:
                if endpoint is not None:
                    endpoint.delete(
                        force=True,
                        sync=True
                    )
                    logger.info(f"Endpoint: {Settings.GCP_ENDPOINT_NAME} deleted successfully.")

                if model is not None:
                    model.delete(
                        sync=True
                    )
                    logger.info("Hugging Face Model Deleted successfully.")
                
                logger.exception("Failed to deploy model to GCP Vertex AI.")
                raise ModelDeploymentException("Failed to deploy model to GCP Vertex AI.") from e


        else:
            logger.info("Requested Infrastructure Not Available")
            logger.info("Deployment Failed.")

            raise AvailabilityException("Deployment Failed due to Infrastructure Availability.")




if __name__=="__main__":
    infrastructure_val=InfrastructureValidator()
    model_reg=ModelRegistrar()
    endpoint_mang=EndpointManager()

    deployment_service=DeploymentService(
        infrastructure_validator=infrastructure_val,
        model_registrar=model_reg,
        endpoint_manager=endpoint_mang
    )

    deployment_service.deploy()