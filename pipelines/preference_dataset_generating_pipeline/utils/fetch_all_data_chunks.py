from concurrent.futures import as_completed,ThreadPoolExecutor

from document_categories.nosql_db_document_categories.base.user_document import UserDocument

from document_categories.vectordb_document_categories.chunked_documents.base.chunked_document import ChunkedDocument
from document_categories.vectordb_document_categories.chunked_documents.article_chunked_document import ArticleChunkedDocument
from document_categories.vectordb_document_categories.chunked_documents.post_chunked_document import PostChunkedDocument
from document_categories.vectordb_document_categories.chunked_documents.tweet_chunked_document import TweetChunkedDocument
from document_categories.vectordb_document_categories.chunked_documents.repository_chunked_document import RepositoryChunkedDocument


def _fetch_article_chunks(user_id:str) -> list[ArticleChunkedDocument]:
    chunks=ArticleChunkedDocument.find_all(author_id=user_id)
    return chunks

def _fetch_post_chunks(user_id:str) -> list[PostChunkedDocument]:
    chunks=PostChunkedDocument.find_all(author_id=user_id)
    return chunks

def _fetch_tweet_chunks(user_id:str) -> list[TweetChunkedDocument]:
    chunks=TweetChunkedDocument.find_all(author_id=user_id)
    return chunks

def _fetch_repository_chunks(user_id:str) -> list[RepositoryChunkedDocument]:
    chunks=RepositoryChunkedDocument.find_all(author_id=user_id)
    return chunks


def fetch_all_chunks(user:UserDocument) -> list[ChunkedDocument]:
    user_id=str(user.id)
    chunked_documents=[]

    with ThreadPoolExecutor() as executor:
        futures=[
            executor.submit(_fetch_article_chunks,user_id),
            executor.submit(_fetch_post_chunks,user_id),
            executor.submit(_fetch_tweet_chunks,user_id),
            executor.submit(_fetch_repository_chunks,user_id)
        ]

        for future in as_completed(futures):
            result=future.result()
            chunked_documents.extend(result)


    return chunked_documents