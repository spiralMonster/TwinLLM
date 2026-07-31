from loguru import logger

from dataset_generator.instruction_dataset_generator.base.instruction_generator import InstructionGenerator
from dataset_generator.instruction_dataset_generator.instruction_generator_from_articles import InstructionGeneratorFromArticles
from dataset_generator.instruction_dataset_generator.instruction_generator_from_posts import InstructionGeneratorFromPosts
from dataset_generator.instruction_dataset_generator.instruction_generator_from_tweets import InstructionGeneratorFromTweets
from dataset_generator.instruction_dataset_generator.instruction_generator_from_repositories import InstructionGeneratorFromRepositories

from document_categories.data_category import DataCategory

from utils.exceptions.general_exceptions.invalid_document_type_exception import InvalidDocumentTypeException


class InstructionGeneratorHandler:
    @staticmethod
    def create_handler(data_category:DataCategory) -> InstructionGenerator:
        if data_category==DataCategory.ARTICLES:
            return InstructionGeneratorFromArticles()
        
        elif data_category==DataCategory.POSTS:
            return InstructionGeneratorFromPosts()
        
        elif data_category==DataCategory.TWEETS:
            return InstructionGeneratorFromTweets()
        
        elif data_category==DataCategory.REPOSITORIES:
            return InstructionGeneratorFromRepositories()
        
        else:
            logger.info("Invalid Document type. Couldn't find appropriate Instruction Data Generator.")
            raise InvalidDocumentTypeException("Invalid Document!!!")