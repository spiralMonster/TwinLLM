import boto3
import json
from pathlib import Path
from loguru import logger

from settings import Settings


def create_sagemaker_user(username:str) -> dict:
    assert Settings.AWS_REGION, "AWS Region is not set."
    assert Settings.AWS_ACCESS_KEY, "AWS_ACCESS_KEY is not set."
    assert Settings.AWS_SECRET_KEY, "AWS_SECRET_KEY is not set."

    iam=boto3.client(
        "iam",
        region_name=Settings.AWS_REGION,
        aws_access_key_id=Settings.AWS_ACCESS_KEY,
        aws_secret_access_key=Settings.AWS_SECRET_KEY
    )

    iam.create_user(UserName=username)

    policies = [
        "arn:aws:iam::aws:policy/AmazonSageMakerFullAccess",
        "arn:aws:iam::aws:policy/AWSCloudFormationFullAccess",
        "arn:aws:iam::aws:policy/IAMFullAccess",
        "arn:aws:iam::aws:policy/AmazonEC2ContainerRegistryFullAccess",
        "arn:aws:iam::aws:policy/AmazonS3FullAccess"
    ]

    for policy in policies:
        iam.attach_user_policy(
            UserName=username,
            PolicyArn=policy
        )


    response=iam.create_access_key(UserName=username)
    access_key=response["AccessKey"]

    logger.info(f" User '{username}' successfully created.")
    logger.info("Access Key ID and Secret Access Key successfully created.")

    result={
        "AccessKeyId":access_key["AccessKeyId"],
        "SecretAccessKey":access_key["SecretAccessKey"]
    }

    return result



if __name__=="__main__":
    new_user=create_sagemaker_user(username="sagemaker-deployer")

    with Path("configs/aws_configs/sagemaker_user_credentials.json").open("w") as f:
        json.dump(new_user,f)

    logger.info("Credentials saved to 'sagemaker_user_credentials.json'")
