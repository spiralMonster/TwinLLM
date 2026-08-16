from loguru import logger

from sagemaker.enums import EndpointType
from sagemaker.huggingface import get_huggingface_llm_image_uri

from model_deployment.aws_deployment.resource_manager.resource_manager import ResourceManager
from model_deployment.aws_deployment.deployment_service.deployment_service import DeploymentService
from model_deployment.aws_deployment.deployment_strategy.sagemaker_huggingface_strategy import SagemakerHuggingFaceStrategy

from model_deployment.aws_deployment.deployment_configs.model_resource_config import model_resource_config
from model_deployment.aws_deployment.deployment_configs.hugging_face_deployment_config import hugging_face_deploy_config

from settings import Settings


def create_endpoint(endpoint_type=EndpointType.INFERENCE_COMPONENT_BASED):
    assert Settings.AWS_ARN_ROLE is not None, "AWS_ARN_ROLE is not set in the .env file."

    logger.info(f"Creating endpoint with endpoint type = {endpoint_type} and model_id = {Settings.DEPLOY_MODEL_ID}")

    llm_image=get_huggingface_llm_image_uri("huggingface")

    resource_manager=ResourceManager()
    deployment_service=DeploymentService(resource_manager=resource_manager)

    SagemakerHuggingFaceStrategy(deployment_service=deployment_service).deploy(
        role_arn=Settings.AWS_ARN_ROLE,
        llm_image=llm_image,
        config=hugging_face_deploy_config,
        endpoint_name=Settings.SAGEMAKER_ENDPOINT_NAME,
        endpoint_config_name=Settings.SAGEMAKER_ENDPOINT_CONFIG_NAME,
        gpu_instance_type=Settings.GPU_INSTANCE,
        resources=model_resource_config,
        endpoint_type=endpoint_type

    )



if __name__=="__main__":
    create_endpoint(endpoint_type=EndpointType.MODEL_BASED)