import enum
from typing import Optional
from loguru import logger

import boto3
from sagemaker.enums import EndpointType
from sagemaker.huggingface import HuggingFaceModel

from model_deployment.aws_deployment.resource_manager.resource_manager import ResourceManager

from utils.exceptions.deployment_exceptions.aws_sagemaker_deployment_exception import SageMakerDeploymentException
from settings import Settings




class DeploymentService:
    def __init__(self,resource_manager:ResourceManager) -> None:
        self.sagemaker_client=boto3.client(
            "sagemaker",
            region_name=Settings.AWS_REGION,
            aws_access_key_id=Settings.AWS_ACCESS_KEY,
            aws_secret_access_key=Settings.AWS_SECRET_KEY
        )

        self.resource_manager=resource_manager



    @staticmethod
    def prepare_and_deploy_model(
            role_arn:str,
            llm_image:str,
            config:dict,
            endpoint_name:str,
            update_endpoint:bool,
            gpu_instance_type:str,
            resources:Optional[dict]=None,
            endpoint_type:enum.Enum=EndpointType.MODEL_BASED
    ) -> None:

        huggingface_model=HuggingFaceModel(
            role=role_arn,
            image_uri=llm_image,
            env=config,
            transformers_version="5.14.1",
            pytorch_version="2.13.0",
            py_version="py311"
        )

        huggingface_model.deploy(
            instance_type=gpu_instance_type,
            initial_instance_count=1,
            endpoint_name=endpoint_name,
            update_endpoint=update_endpoint,
            resources=resources,
            tags=[{"Key":"task","Value":"model_task"}],
            endpoint_type=endpoint_type,
            container_startup_health_check_timeout=900
        )



    def deploy(
            self,
            role_arn:str,
            llm_image:str,
            config:dict,
            endpoint_name:str,
            endpoint_config_name:str,
            gpu_instance_type:str,
            resources:Optional[dict]=None,
            endpoint_type:enum.Enum=EndpointType.MODEL_BASED
    ) -> None:

        try:
            if self.resource_manager.endpoint_config_exists(endpoint_config_name=endpoint_config_name):
                logger.info(f"Endpoint Configuration {endpoint_config_name} exists. Using existing configuration.")

            else:
                logger.info(f"Endpoint Configuration {endpoint_config_name} does not exist.")


            self.prepare_and_deploy_model(
                role_arn=role_arn,
                llm_image=llm_image,
                config=config,
                endpoint_name=endpoint_name,
                update_endpoint=False,
                resources=resources,
                gpu_instance_type=gpu_instance_type,
                endpoint_type=endpoint_type
            )
            logger.info(f"Successfully deployed/updated model to endpoint {endpoint_name}.")


        except Exception as e:
            logger.info(f"Exception encountered: {e}")
            raise SageMakerDeploymentException("Failed to deploy model to SageMaker.")

