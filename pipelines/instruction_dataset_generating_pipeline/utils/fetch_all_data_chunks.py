from concurrent.futures import ThreadPoolExecutor,as_completed

from document_categories.nosql_db_document_categories.base.user_document import UserDocument

from document_categories.vectordb_document_categories.chunked_documents.base.chunked_document import ChunkedDocument
from document_categories.vectordb_document_categories.chunked_documents.article_chunked_document import ArticleChunkedDocument
from document_categories.vectordb_document_categories.chunked_documents.post_chunked_document import PostChunkedDocument
from document_categories.vectordb_document_categories.chunked_documents.tweet_chunked_document import TweetChunkedDocument
from document_categories.vectordb_document_categories.chunked_documents.repository_chunked_document import RepositoryChunkedDocument


def _fetch_article_chunks(user_id:str) -> list[ArticleChunkedDocument]:
    article_chunks=ArticleChunkedDocument.find_all(author_id=user_id)
    return article_chunks

def _fetch_post_chunks(user_id:str) -> list[PostChunkedDocument]:
    post_chunks=PostChunkedDocument.find_all(author_id=user_id)
    return post_chunks

def _fetch_tweet_chunks(user_id:str) -> list[TweetChunkedDocument]:
    tweet_chunks=TweetChunkedDocument.find_all(author_id=user_id)
    return tweet_chunks

def _fetch_repository_chunks(user_id:str) -> list[RepositoryChunkedDocument]:
    repo_chunks=RepositoryChunkedDocument.find_all(author_id=user_id)
    return repo_chunks



def fetch_all_chunks(user:UserDocument) -> list[ChunkedDocument]:
    user_id=str(user.id)
    chunks=[]

    with ThreadPoolExecutor() as executor:
        futures=[
            executor.submit(_fetch_article_chunks,user_id),
            executor.submit(_fetch_post_chunks,user_id),
            executor.submit(_fetch_tweet_chunks,user_id),
            executor.submit(_fetch_repository_chunks,user_id)
        ]

        for future in as_completed(futures):
            chunks.extend(future.result())


    return chunks


