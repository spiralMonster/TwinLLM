from loguru import logger

from document_categories import data_category
from document_categories.data_category import DataCategory

category=DataCategory("posts")

if category==DataCategory.POSTS:
    logger.info(
        "Demo",
        data_category=category
    )


else:
    print("No")