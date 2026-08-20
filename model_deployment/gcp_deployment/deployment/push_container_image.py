from loguru import logger
import subprocess

from google.cloud import artifactregistry_v1
from google.api_core.exceptions import NotFound

from utils.exceptions.deployment_exceptions.gcp_exceptions.image_pusher_exception import ImagePusherException

from settings import Settings


class ContainerImagePusher:
    def __init__(self):
        self.client=artifactregistry_v1.ArtifactRegistryClient()


    @staticmethod
    def get_image_uri() -> str:
        image_uri=(
            f"{Settings.GCP_REGION}-docker.pkg.dev/"
            f"{Settings.GCP_PROJECT_ID}/"
            f"{Settings.GCP_REPOSITORY_NAME}/"
            f"{Settings.CUSTOM_PYTORCH_INFERENCE_IMAGE}"
        )

        return image_uri


    def create_repository(self) -> None:
        parent=(
            f"projects/{Settings.GCP_PROJECT_ID}"
            f"/locations/{Settings.GCP_REGION}"
        )

        repository_name=(
            f"{parent}"
            f"/repositories/{Settings.GCP_REPOSITORY_NAME}"
        )

        try:
            repository=self.client.get_repository(
                name=repository_name
            )

            logger.info(f"Repository already exists: {repository.name}")

        except NotFound:
            logger.info("Repository does not exist")
            logger.info(f"Creating: {repository_name}")

            repository=artifactregistry_v1.Repository(
                name=repository_name,
                format_=artifactregistry_v1.Repository.Format.DOCKER,
                description="Twin LLM Docker Imager"
            )
            operation=self.client.create_repository(
                parent=parent,
                repository=repository,
                repository_id=Settings.GCP_REPOSITORY_NAME
            )

            repository=operation.result()
            logger.info(f"Repository created successfully: {repository.name}")




    @staticmethod
    def configure_docker() -> None:
        subprocess.run(
            [
                "gcloud",
                "auth",
                "configure-docker",
                f"{Settings.GCP_REGION}-docker.pkg.dev",
            ],
            check=True
        )


    def push_image(self):
        local_image=Settings.CUSTOM_PYTORCH_INFERENCE_IMAGE
        remote_image=self.get_image_uri()

        try:
            self.create_repository()
            self.configure_docker()

            logger.info("Tagging image...")

            subprocess.run(
                [
                    "docker",
                    "tag",
                    local_image,
                    remote_image
                ],
                check=True
            )

            logger.info("Pushing Image...")
            subprocess.run(
                [
                    "docker",
                    "push",
                    remote_image
                ],
                check=True
            )


        except Exception as e:
            logger.exception(
                f"Failed to push local image: {local_image}"
            )

            raise ImagePusherException(
                "Failed to push the local image to GCP."
            ) from e



    def delete_repository(self) -> None:
        parent=(
            f"projects/{Settings.GCP_PROJECT_ID}"
            f"/locations/{Settings.GCP_REGION}"
        )

        repo_name=(
            f"{parent}"
            f"/repositories/{Settings.GCP_REPOSITORY_NAME}"
        )

        try:
            logger.info(f"Deleting Artifact Registry Repository: {repo_name}")

            operation=self.client.delete_repository(
                name=repo_name
            )
            operation.result()

            logger.info(f"Artifact Registry repository deleted successfully: {repo_name}")

        except NotFound:
            logger.info(
                f"Artifact Registry repository does not exist: {repo_name}"
                "Nothing to clean."
            )

        except Exception as e:
            logger.info(f"Exception encountered: {e}")
            logger.exception(f"Failed to delete the Artifact Registry repository: {repo_name}")

