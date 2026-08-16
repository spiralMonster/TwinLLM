from loguru import logger

import boto3
from botocore.exceptions import ClientError

from settings import Settings


def delete_endpoint_and_config(endpoint_name:str) -> None:
    try:
        sagemaker_client=boto3.client(
            "sagemaker",
            region_name=Settings.AWS_REGION,
            aws_access_key_id=Settings.AWS_ACCESS_KEY,
            aws_secret_access_key=Settings.AWS_SECRET_KEY
        )

    except Exception as e:
        logger.info(f"Exception Encountered: {e}")
        return


    try:
        response=sagemaker_client.describe_endpoint(EndpointName=endpoint_name)
        config_name=response["EndpointConfigName"]

    except ClientError:
        logger.info("Error getting endpoint configuration")
        return


    try:
        sagemaker_client.delete_endpoint(EndpointName=endpoint_name)
        logger.info(f"Endpoint '{endpoint_name}' deletion initiated.")

    except ClientError:
        logger.info("Error deleting Endpoint.")


    try:
        response=sagemaker_client.describe_endpoint_config(EndpointConfigName=config_name)
        model_name=response["ProductionVariants"][0]["ModelName"]

    except ClientError:
        logger.info("Error getting model name.")
        return


    try:
        sagemaker_client.delete_endpoint_config(EndpointConfigName=config_name)
        logger.info(f"Endpoint configuration '{config_name}' deleted.")

    except ClientError:
        logger.info("Error deleting endpoint configuration.")


    try:
        sagemaker_client.delete_model(ModelName=model_name)
        logger.info(f"Model '{model_name}' deleted.")

    except ClientError:
        logger.info("Error deleting model.")



if __name__=="__main__":
    endpoint_name=Settings.SAGEMAKER_ENDPOINT_NAME
    logger.info(f"Attempting to delete SageMaker endpoint: {endpoint_name}")
    delete_endpoint_and_config(endpoint_name=endpoint_name)


