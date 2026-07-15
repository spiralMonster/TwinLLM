from loguru import logger
from typing import Annotated

from zenml import step,get_step_context

from document_categories.nosql_db_document_categories.user_document import UserDocument

from pipelines.data_etl_pipeline.metadata.get_or_create_user_metadata import _get_metadata


@step
def get_or_create_user(user_full_name: str) -> Annotated[UserDocument,"user"]:
    logger.info(f"Getting or creating user: {user_full_name}")

    user_details=user_full_name.split(" ")
    user_first_name=user_details[0]
    user_last_name=user_details[1]

    user=UserDocument(
        first_name=user_first_name,
        last_name=user_last_name
    )

    metadata=_get_metadata(
        user_full_name=user_full_name,
        user=user
    )

    step_context=get_step_context()
    step_context.add_output_metadata(
        output_name="user",
        metadata=metadata
    )

    return user


