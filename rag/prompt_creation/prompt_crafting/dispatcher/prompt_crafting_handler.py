from loguru import logger

from rag.prompt_creation.prompt_crafting.craft_from.base.craft_prompt import CraftPrompt
from rag.prompt_creation.prompt_crafting.craft_from.articles import CraftPromptFromArticles
from rag.prompt_creation.prompt_crafting.craft_from.posts import CraftPromptFromPosts
from rag.prompt_creation.prompt_crafting.craft_from.repositories import CraftPromptFromRepositories
from rag.prompt_creation.prompt_crafting.craft_from.tweets import CraftPromptFromTweets

from document_categories.data_category import DataCategory
from utils.exceptions.general_exceptions.invalid_document_type_exception import InvalidDocumentTypeException


class PromptCraftingHandler:
    @staticmethod
    def create_handler(data_category:DataCategory) -> CraftPrompt:
        if data_category==DataCategory.ARTICLES:
            return CraftPromptFromArticles()
        
        elif data_category==DataCategory.POSTS:
            return CraftPromptFromPosts()
        
        elif data_category==DataCategory.REPOSITORIES:
            return CraftPromptFromRepositories()
        
        elif data_category==DataCategory.TWEETS:
            return  CraftPromptFromTweets()
        
        else:
            logger.info("Invalid Document type. Couldn't find appropriate Prompt Crafter.")
            raise InvalidDocumentTypeException("Invalid Document!!!")
            