from loguru import logger

from google.auth import default
from googleapiclient.discovery import build

from settings import Settings

SERVICES=[
    "aiplatform.googleapis.com",
    "compute.googleapis.com",
    "container.googleapis.com",
    "containerregistry.googleapis.com",
    "containerfilesystem.googleapis.com",
]


def enable_services() -> None:
    credentials,_=default(
        scopes=["https://www.googleapis.com/auth/cloud-platform"]
    )

    service_usage=build(
        "serviceusage",
        "v1",
        credentials=credentials
    )
    project_name=f"projects/{Settings.GCP_PROJECT_ID}"
    logger.info(f"Enabling services for GCP Project: {project_name}")

    for service in SERVICES:
        print(f"Enabling {service}...")

        operation=(
            service_usage.services()
            .enable(
                name=f"{project_name}/services/{service}"
            )
            .execute()
        )

        print(
            f"Enable operation started for {service}: "
            f"{operation.get('name')}"
        )



if __name__=="__main__":
    enable_services()