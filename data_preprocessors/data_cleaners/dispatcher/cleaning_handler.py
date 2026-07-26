from loguru import logger

from data_preprocessors.data_cleaners.base.data_cleaner import DataCleaner
from data_preprocessors.data_cleaners.post_data_cleaner import PostDataCleaner
from data_preprocessors.data_cleaners.article_data_cleaner import ArticleDataCleaner
from data_preprocessors.data_cleaners.repository_data_cleaner import RepositoryDataCleaner
from data_preprocessors.data_cleaners.tweet_data_cleaner import TweetDataCleaner

from document_categories.data_category import DataCategory

from utils.exceptions.general_exceptions.invalid_document_type_exception import InvalidDocumentTypeException


class CleaningHandler:
    @staticmethod
    def create_handler(data_category:DataCategory) -> DataCleaner:
        if data_category==DataCategory.POSTS:
            return PostDataCleaner()

        elif data_category==DataCategory.ARTICLES:
            return ArticleDataCleaner()

        elif data_category==DataCategory.REPOSITORIES:
            return RepositoryDataCleaner()

        elif data_category==DataCategory.TWEETS:
            return TweetDataCleaner()

        else:
            logger.info("Invalid Document type. Couldn't find appropriate Data Cleaner.")
            raise InvalidDocumentTypeException("Invalid Document!!!")

