from loguru import logger

from data_preprocessors.data_embedders.base.data_embedder import DataEmbedder
from data_preprocessors.data_embedders.post_data_embedder import PostDataEmbedder
from data_preprocessors.data_embedders.article_data_embedder import ArticleDataEmbedder
from data_preprocessors.data_embedders.repository_data_embedder import RepositoryDataEmbedder
from data_preprocessors.data_embedders.tweet_data_embedder import TweetDataEmbedder

from document_categories.data_category import DataCategory

from utils.exceptions.general_exceptions.invalid_document_type_exception import InvalidDocumentTypeException


class EmbeddingHandler:
    @staticmethod
    def create_handler(data_category:DataCategory) -> DataEmbedder:
        if data_category==DataCategory.POSTS:
            return PostDataEmbedder()

        elif data_category==DataCategory.ARTICLES:
            return ArticleDataEmbedder()

        elif data_category==DataCategory.REPOSITORIES:
            return RepositoryDataEmbedder()

        elif data_category==DataCategory.TWEETS:
            return TweetDataEmbedder()

        else:
            logger.info("Invalid Document type. Couldn't find appropriate Data Embedder.")
            raise InvalidDocumentTypeException("Invalid Document!!!")
