from loguru import logger
from concurrent.futures.thread import ThreadPoolExecutor
from asyncio import as_completed

from document_categories.nosql_db_document_categories.base.user_document import UserDocument
from document_categories.nosql_db_document_categories.base.base_document import Document
from document_categories.nosql_db_document_categories.post_document import PostDocument
from document_categories.nosql_db_document_categories.article_document import ArticleDocument
from document_categories.nosql_db_document_categories.repository_document import RepositoryDocument
from document_categories.nosql_db_document_categories.tweet_document import TweetDocument


def __fetch_articles(user_id:str) -> list[ArticleDocument]:
    article_docs=ArticleDocument.bulk_find(author_id=user_id)
    return article_docs


def __fetch_posts(user_id:str) -> list[PostDocument]:
    post_docs=PostDocument.bulk_find(author_id=user_id)
    return post_docs


def __fetch_repositories(user_id:str) -> list[RepositoryDocument]:
    repo_docs=RepositoryDocument.bulk_find(author_id=user_id)
    return repo_docs


def __fetch_tweets(user_id:str) -> list[TweetDocument]:
    tweet_docs=TweetDocument.bulk_find(author_id=user_id)
    return tweet_docs



def fetch_all_data(user:UserDocument) -> dict[str,list[Document]]:
    user_id=str(user.id)

    with ThreadPoolExecutor() as executor:
        future_to_query={
            executor.submit(__fetch_posts,user_id):"posts",
            executor.submit(__fetch_articles,user_id):"articles",
            executor.submit(__fetch_repositories,user_id):"repositories",
            executor.submit(__fetch_tweets,user_id):"tweets"

        }

        results={}
        for future in as_completed(future_to_query):
            query_name=future_to_query[future]
            try:
                results[query_name]=future.result()

            except Exception:
                logger.exception(f"Couldn't find {query_name} of user: {user.full_name}")
                results[query_name]=[]


    return results
