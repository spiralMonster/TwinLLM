from loguru import logger
from google.cloud import aiplatform

from utils.exceptions.deployment_exceptions.gcp_exceptions.vertex_ai_exception import VertexAIException
from utils.exceptions.deployment_exceptions.gcp_exceptions.endpoint_creation_exception import EndpointCreationException
from utils.exceptions.deployment_exceptions.gcp_exceptions.endpoint_not_found_exception import EndpointNotFoundException
from utils.exceptions.deployment_exceptions.gcp_exceptions.many_endpoint_found_exception import ManyEndPointFoundException

from settings import Settings



class EndpointManager:
    def __init__(self) -> None:
        aiplatform.init(
            project=Settings.GCP_PROJECT_ID,
            location=Settings.GCP_REGION
        )


    @staticmethod
    def create_endpoint() -> aiplatform.Endpoint:
        logger.info(f"Creating Vertex AI Endpoint: {Settings.GCP_ENDPOINT_NAME}")

        try:
            endpoint=aiplatform.Endpoint.create(
                display_name=Settings.GCP_ENDPOINT_NAME
            )
            endpoint.wait()

            logger.info(f"Successfully created the Vertex AI Endpoint: {Settings.GCP_ENDPOINT_NAME}")

            return endpoint

        except Exception as e:
            logger.info(f"Exception Encountered: {e}")
            raise EndpointCreationException("Failed to create the Endpoint.")


    @staticmethod
    def get_endpoint() -> aiplatform.Endpoint:
        try:
            logger.info(f"Fetching Vertex AI Endpoint: {Settings.GCP_ENDPOINT_NAME}")

            endpoints=aiplatform.Endpoint.list(
                filter=(
                    f'display_name="{Settings.GCP_ENDPOINT_NAME}"'
                )
            )

            if not endpoints:
                logger.exception("Couldn't find the Endpoint.")
                raise EndpointNotFoundException(f"Endpoint: {Settings.GCP_ENDPOINT_NAME} was not found...")

            if len(endpoints)>1:
                logger.exception("Found multiple Endpoints")
                raise ManyEndPointFoundException(f"Multiple endpoints found with display name: {Settings.GCP_ENDPOINT_NAME}")

            endpoint=endpoints[0]

            logger.info(f"Endpoint with display name: {Settings.GCP_ENDPOINT_NAME} fetched successfully.")
            return endpoint

        except Exception as e:
            logger.exception("Failed to fetch Vertex AI Endpoint")

            raise VertexAIException(
                "Failed to fetch Vertex AI endpoint."
            ) from e




