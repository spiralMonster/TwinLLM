import re
import hashlib
from uuid import UUID
from loguru import logger

from document_categories.vectordb_document_categories.cleaned_documents.cleaned_post_document import CleanedPostDocument
from document_categories.vectordb_document_categories.chunked_documents.post_chunked_document import PostChunkedDocument

from data_preprocessors.data_chunkers.base.data_chunker import DataChunker



class PostDataChunker(DataChunker):
    @property
    def metadata(self) -> dict:
        _metadata={
            "maximum_chunk_size":400,
            "chunk_overlap":100,
            "minimum_chunk_size":80
        }

        return _metadata



    def chunk(self,cleaned_document:CleanedPostDocument) -> list[PostChunkedDocument]:
        cleaned_content=cleaned_document.content

        #Splitting text:
        sentences=re.split(r"\n\n+",cleaned_content)

        minimum_chunk_size=self.metadata["minimum_chunk_size"]
        maximum_chunk_size=self.metadata["maximum_chunk_size"]
        chunk_overlap=self.metadata["chunk_overlap"]

        split_expression_based_on_punctuation=r"(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?|\!)\s"

        sentences_to_chunk=[]
        chunked_sentences=[]
        for sent in sentences:
            if len(sent)<=maximum_chunk_size:
                if len(sent)>=minimum_chunk_size:
                    chunked_sentences.append(sent)

            else:
                s=re.split(split_expression_based_on_punctuation,sent)
                sentences_to_chunk.extend(s)


        chunks=self._chunk(
            sentences=sentences_to_chunk,
            min_chunk_length=minimum_chunk_size,
            max_chunk_length=maximum_chunk_size,
            chunk_overlap=chunk_overlap
        )
        chunked_sentences.extend(chunks)

        chunked_documents=[]
        for chunk in chunked_sentences:
            chunk_id=hashlib.md5(chunk.encode()).hexdigest()
            chunk_id=UUID(chunk_id,version=4)

            chunk_doc=PostChunkedDocument(
                id=chunk_id,
                content=chunk,
                document_id=cleaned_document.id,
                platform=cleaned_document.platform,
                author_id=cleaned_document.author_id,
                author_full_name=cleaned_document.author_full_name,
                metadata=self.metadata,
                username=cleaned_document.username,
                link=cleaned_document.link,
                published_date=cleaned_document.published_date

            )
            chunked_documents.append(chunk_doc)


        chunk_len=len(chunked_documents)
        logger.info(f"The cleaned post: {cleaned_document.link} is chunked into {chunk_len} chunks successfully.")

        return chunked_documents


