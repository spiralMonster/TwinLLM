import os

from loguru import logger
from pathlib import Path

from google.cloud import storage
from google.api_core.exceptions import NotFound

from huggingface_hub import snapshot_download

from utils.exceptions.model_exceptions.hugging_face_exception import HuggingFaceException
from utils.exceptions.deployment_exceptions.gcp_exceptions.model_uploader_excpetion import ModelUploaderException

from settings import Settings


class ModelUploader:
    def __init__(self) -> None:
        self.client=storage.Client(
            project=Settings.GCP_PROJECT_ID
        )

        self.bucket=self.client.bucket(
            bucket_name=Settings.GCP_BUCKET_NAME
        )

        self.local_model_dir=Path("artifacts/model")



    def download_model(self) -> None:
        logger.info(f"Downloading Model: {Settings.DEPLOY_MODEL_ID} from Hugging Face Hub locally.")

        local_dir=self.local_model_dir
        if not local_dir.exists():
            raise FileNotFoundError(
                f"Model directory: {local_dir} does not exist"
            )

        if not local_dir.is_dir():
            raise ValueError(
                f"Model path: {local_dir} is not directory"
            )

        try:
            snapshot_download(
                repo_id=Settings.DEPLOY_MODEL_ID,
                local_dir=local_dir,
                token=Settings.HF_TOKEN
            )
            logger.info(f"Model downloaded to : {self.local_model_dir}")

        except Exception as e:
            logger.exception("Failed to download the model.")
            raise HuggingFaceException(
                "Failed to download the model from the Hugging Face Hub locally."
            ) from e



    @staticmethod
    def get_model_artifact_uri() -> tuple[str,str]:
        gcs_prefix=(
            f"{Settings.GCP_MODEL_ARTIFACT_PREFIX}/"
            f"{Settings.DEPLOY_MODEL_ID.replace('/','--')}"
        )

        gcs_uri=f"gs://{Settings.GCP_BUCKET_NAME}/{gcs_prefix}"
        return gcs_prefix,gcs_uri



    def upload_model(self) -> None:
        try:
            gcs_prefix,gcs_uri=self.get_model_artifact_uri()
            local_model_dir=self.local_model_dir

            if not local_model_dir.exists():
                os.makedirs(local_model_dir,exist_ok=True)
                self.download_model()

            logger.info(f"Uploading model from {local_model_dir} to {gcs_uri}")

            for file_path in local_model_dir.rglob("*"):
                if not file_path.is_file():
                    continue

                relative_path=file_path.relative_to(local_model_dir)

                blob_name=f"{gcs_prefix}/{relative_path.as_posix()}"
                blob=self.bucket.blob(blob_name)

                logger.info(f"Uploading: {relative_path}")
                blob.upload_from_filename(str(file_path))


            logger.info(f"Model : {Settings.DEPLOY_MODEL_ID} uploaded successfully to: {gcs_uri}")

        except Exception as e:
            logger.exception("Failed to upload the Model.")
            raise ModelUploaderException(
                "Failed to upload the model to GCP Storage."
            ) from e



    def delete_model_artifacts(self) -> None:
        try:
            logger.info(f"Cleaning up GCS bucket: {Settings.GCP_BUCKET_NAME}")

            try:
                blobs=self.bucket.list_blobs()
                deleted_count=0

                for blob in blobs:
                    logger.info(f"Deleting GCS object: {blob.name}")

                    blob.delete()
                    deleted_count+=1


                logger.info(
                    f"Deleted {deleted_count} objects from"
                    f"bucket: {Settings.GCP_BUCKET_NAME}"
                )
                logger.info(f"Deleting GCP bucket: {Settings.GCP_BUCKET_NAME}")

                self.bucket.delete()
                logger.info(f"GCS bucket deleted successfully: {Settings.GCP_BUCKET_NAME}")


            except NotFound:
                logger.info(
                    f"GCS bucket: {Settings.GCP_BUCKET_NAME} does not exist"
                    "Nothing to clean."
                )


        except Exception as e:
            logger.info(f"Exception encountered: {e}")
            logger.info(f"Failed to delete the GCP bucket: {Settings.GCP_BUCKET_NAME}")

