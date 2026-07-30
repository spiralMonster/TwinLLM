import re
import hashlib
from uuid import UUID
from loguru import logger

from document_categories.vectordb_document_categories.cleaned_documents.cleaned_article_document import CleanedArticleDocument
from document_categories.vectordb_document_categories.chunked_documents.article_chunked_document import ArticleChunkedDocument

from data_preprocessors.data_chunkers.base.data_chunker import DataChunker


class ArticleDataChunker(DataChunker):
    @property
    def metadata(self) -> dict:
        _metadata={
            "maximum_chunk_size":1000,
            "chunk_overlap":200,
            "minimum_chunk_size":250
        }

        return _metadata



    def chunk(self,cleaned_document:CleanedArticleDocument) -> list[ArticleChunkedDocument]:
        cleaned_content=cleaned_document.content

        #Splitting the text:
        split_expression=r"(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?|\!)\s"
        sentences=re.split(split_expression,cleaned_content)

        chunks=self._chunk(
            sentences=sentences,
            min_chunk_length=self.metadata["minimum_chunk_size"],
            max_chunk_length=self.metadata["maximum_chunk_size"],
            chunk_overlap=self.metadata["chunk_overlap"]
        )


        chunked_documents=[]
        for chunk in chunks:
            chunk_id=hashlib.md5(chunk.encode()).hexdigest()
            chunk_id=UUID(chunk_id,version=4)

            chunk_doc=ArticleChunkedDocument(
                id=chunk_id,
                content=chunk,
                platform=cleaned_document.platform,
                author_id=cleaned_document.author_id,
                author_full_name=cleaned_document.author_full_name,
                document_id=cleaned_document.id,
                metadata=self.metadata,
                username=cleaned_document.username,
                link=cleaned_document.link,
                title=cleaned_document.title,
                description=cleaned_document.description,
                published_date=cleaned_document.published_date

            )
            chunked_documents.append(chunk_doc)


        len_chunks=len(chunked_documents)
        logger.info(f"The cleaned article: {cleaned_document.link} is chunked into {len_chunks} chunks.")

        return chunked_documents





