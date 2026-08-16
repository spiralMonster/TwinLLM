import boto3
import json
from pathlib import Path
from loguru import logger

from settings import Settings


def create_sagemaker_execution_role(role_name:str) -> dict:
    assert Settings.AWS_REGION, "AWS_REGION is not set."
    assert Settings.AWS_ACCESS_KEY, "AWS_ACCESS_KEY is not set."
    assert Settings.AWS_SECRET_KEY, "AWS_SECRET_KEY is not set."

    iam=boto3.client(
        "iam",
        region_name=Settings.AWS_REGION,
        aws_access_key_id=Settings.AWS_ACCESS_KEY,
        aws_secret_access_key=Settings.AWS_SECRET_KEY
    )

    trust_relationship={
        "Version":"2012-10-17",
        "Statement":[
            {
                "Effect":"Allow",
                "Principal":{
                    "Service":"sagemaker.amazonaws.com"
                },
                "Action":"sts:AssumeRole"
            }
        ]
    }

    try:
        role=iam.create_role(
            RoleName=role_name,
            AssumeRolePolicyDocument=json.dumps(trust_relationship),
            Description="Execution role for SageMaker"
        )

        policies=[
        "arn:aws:iam::aws:policy/AmazonSageMakerFullAccess",
        "arn:aws:iam::aws:policy/AmazonS3FullAccess",
        "arn:aws:iam::aws:policy/CloudWatchLogsFullAccess",
        "arn:aws:iam::aws:policy/AmazonEC2ContainerRegistryFullAccess",
        ]

        for policy in policies:
            iam.attach_role_policy(
                RoleName=role_name,
                PolicyArn=policy
            )

        logger.info(f"Role '{role_name}' created successfully.")
        logger.info(f"Role ARN: {role['Role']['Arn']}")

        result={
            "RoleArn":role["Role"]["Arn"]
        }

        return result

    except iam.exceptions.EntityAlreadyExistsException:
        logger.warning(f"Role '{role_name}' already exists. Fetching its ARN..")
        role=iam.get_role(RoleName=role_name)

        result={
            "RoleArn":role["Role"]["Arn"]
        }

        return result



if __name__=="__main__":
    role_arn=create_sagemaker_execution_role(role_name="SageMakerExecutionRole")

    with Path("configs/aws_configs/sagemaker_execution_role.json").open("w") as f:
        json.dump(role_arn,f)


    logger.info("Role ARN saved to 'sagemaker_execution_role.json'")