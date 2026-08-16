from loguru import logger

import boto3
from botocore.exceptions import ClientError
from sympy import true

from settings import Settings


class ResourceManager:
    def __init__(self) -> None:
        self.sagemaker_client=boto3.client(
            "sagemaker",
            region_name=Settings.AWS_REGION,
            aws_access_key_id=Settings.AWS_ACCESS_KEY,
            aws_secret_access_key=Settings.AWS_SECRET_KEY
        )


    def endpoint_config_exists(self,endpoint_config_name:str) -> bool:
        try:
            self.sagemaker_client.describe_endpoint_config(EndpointConfigName=endpoint_config_name)
            logger.info(f"Endpoint configuration '{endpoint_config_name}' exists.")
            return True

        except ClientError:
            logger.info(f"Endpoint configuration '{endpoint_config_name}' does not exist.")
            return False



    def endpoint_exists(self,endpoint_name:str) -> bool:
        try:
            self.sagemaker_client.describe_endpoint(EndpointName=endpoint_name)
            logger.info(f"Endpoint '{endpoint_name} exists.'")
            return True

        except ClientError:
            logger.info(f"Endpoint '{endpoint_name}' does not exists.")
            return False