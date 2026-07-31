from loguru import logger

from data_preprocessors.data_chunkers.base.data_chunker import DataChunker
from data_preprocessors.data_chunkers.post_data_chunker import PostDataChunker
from data_preprocessors.data_chunkers.article_data_chunker import ArticleDataChunker
from data_preprocessors.data_chunkers.repository_data_chunker import RepositoryDataChunker
from data_preprocessors.data_chunkers.tweet_data_chunker import TweetDataChunker

from document_categories.data_category import DataCategory

from utils.exceptions.general_exceptions.invalid_document_type_exception import InvalidDocumentTypeException


class ChunkingHandler:
    @staticmethod
    def create_handler(data_category:DataCategory) -> DataChunker:
        if data_category==DataCategory.POSTS:
            return PostDataChunker()

        elif data_category==DataCategory.ARTICLES:
            return ArticleDataChunker()

        elif data_category==DataCategory.REPOSITORIES:
            return RepositoryDataChunker()

        elif data_category==DataCategory.TWEETS:
            return TweetDataChunker()

        else:
            logger.info("Invalid Document type. Couldn't find appropriate Data Cleaner.")
            raise InvalidDocumentTypeException("Invalid Document!!!")
