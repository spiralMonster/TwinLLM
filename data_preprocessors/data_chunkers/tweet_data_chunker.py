import hashlib
from uuid import UUID
from loguru import logger

from langchain.text_splitter import RecursiveCharacterTextSplitter

from document_categories.vectordb_document_categories.cleaned_documents.cleaned_tweet_document import CleanedTweetDocument
from document_categories.vectordb_document_categories.chunked_documents.tweet_chunked_document import TweetChunkedDocument

from data_preprocessors.data_chunkers.base.data_chunker import DataChunker


class TweetDataChunker(DataChunker):
    post_chunk_cleaning=False

    @property
    def metadata(self) -> dict:
        _metadata={
            "chunk_size":200,
            "chunk_overlap":50,
            "minimum_chunk_size":40
        }

        return _metadata


    def chunk(self,cleaned_document:CleanedTweetDocument) ->list[TweetChunkedDocument]:
        cleaned_content=cleaned_document.content

        maximum_chunk_size=self.metadata["chunk_size"]
        minimum_chunk_size=self.metadata["minimum_chunk_size"]
        chunk_overlap=self.metadata["chunk_overlap"]

        character_splitter=RecursiveCharacterTextSplitter(
            chunk_size=maximum_chunk_size,
            chunk_overlap=chunk_overlap
        )

        chunks=character_splitter.split_text(cleaned_content)

        chunked_texts=[]
        for chunk in chunks:
            if len(chunk)>=minimum_chunk_size:
                chunked_texts.append(chunk)


        if self.post_chunk_cleaning:
            cleaned_chunks=[
                self.clean_chunks(chunk=c)
                for c in chunked_texts
            ]
            chunked_texts=cleaned_chunks

        chunked_docs=[]
        for chunk in chunked_texts:
            chunk_id=hashlib.md5(chunk.encode()).hexdigest()
            chunk_id=UUID(chunk_id,version=4)

            chunked_doc=TweetChunkedDocument(
                id=chunk_id,
                content=chunk,
                platform=cleaned_document.platform,
                document_id=cleaned_document.id,
                author_id=cleaned_document.author_id,
                author_full_name=cleaned_document.author_full_name,
                metadata=self.metadata,
                username=cleaned_document.username,
                link=cleaned_document.link,
                published_date=cleaned_document.published_date
            )
            chunked_docs.append(chunked_doc)


        len_chunks=len(chunked_docs)
        logger.info(f"The cleaned tweet document: {cleaned_document.link} is chunked into {len_chunks} chunks successfully.")

        return chunked_docs



