from loguru import logger

from dataset_generator.preference_dataset_generator.base.preference_dataset_generator import PreferenceDatasetGenerator
from dataset_generator.preference_dataset_generator.preference_dataset_generator_from_articles import PreferenceDatasetGeneratorFromArticles
from dataset_generator.preference_dataset_generator.preference_dataset_generator_from_posts import PreferenceDatasetGeneratorFromPosts
from dataset_generator.preference_dataset_generator.preference_dataset_generator_from_tweets import PreferenceDatasetGeneratorFromTweets
from dataset_generator.preference_dataset_generator.preference_dataset_generator_from_repositories import PreferenceDatasetGeneratorFromRepositories

from document_categories.data_category import DataCategory
from utils.exceptions.general_exceptions.invalid_document_type_exception import InvalidDocumentTypeException


class PreferenceDatasetGenHandler:
    @staticmethod
    def create_handler(data_category:DataCategory) -> PreferenceDatasetGenerator:
        if data_category==DataCategory.ARTICLES:
            return PreferenceDatasetGeneratorFromArticles()
        
        elif data_category==DataCategory.POSTS:
            return PreferenceDatasetGeneratorFromPosts()
        
        elif data_category==DataCategory.REPOSITORIES:
            return PreferenceDatasetGeneratorFromRepositories()
        
        elif data_category==DataCategory.TWEETS:
            return PreferenceDatasetGeneratorFromTweets()
        
        else:
            logger.info("Invalid Document type. Couldn't find appropriate Preference Data Generator.")
            raise InvalidDocumentTypeException("Invalid Document!!!")
            