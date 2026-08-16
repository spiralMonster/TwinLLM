import enum
from typing import Optional
from loguru import logger

from sagemaker.enums import EndpointType

from model_deployment.aws_deployment.deployment_service.deployment_service import DeploymentService
from model_deployment.aws_deployment.deployment_strategy.base.deployment_strategy import DeploymentStrategy

from utils.exceptions.deployment_exceptions.aws_sagemaker_deployment_exception import SageMakerDeploymentException
from settings import Settings


class SagemakerHuggingFaceStrategy(DeploymentStrategy):
    def __init__(self,deployment_service:DeploymentService) -> None:
        self.deployment_service=deployment_service


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

        logger.info("Starting deployment using SageMaker HuggingFace Strategy.")
        print("Deployment Parameters:")
        print(f"Number of Replicas: {Settings.NUM_OF_REPLICAS}")
        print(f"Number of CPU Cores: {Settings.NUM_OF_CPU_CORES}")
        print(f"Number of GPU: {Settings.NUM_OF_GPU}")
        print(f"GPU Instance: {Settings.GPU_INSTANCE}")
        print(f"Memory (In MB): {Settings.MIN_MEMORY}")

        try:
            self.deployment_service.deploy(
                role_arn=role_arn,
                llm_image=llm_image,
                config=config,
                endpoint_name=endpoint_name,
                endpoint_config_name=endpoint_config_name,
                gpu_instance_type=gpu_instance_type,
                resources=resources,
                endpoint_type=endpoint_type
            )
            logger.info("Deployment Completed Successfully.")

        except Exception as e:
            logger.info(f"Exception Encountered: {e}")
            raise SageMakerDeploymentException("Failed to deploy model on AWS SageMaker.")


