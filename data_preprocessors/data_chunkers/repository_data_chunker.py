import re
import hashlib
from uuid import UUID
from loguru import logger

from langchain.text_splitter import RecursiveCharacterTextSplitter

from document_categories.vectordb_document_categories.cleaned_documents.cleaned_repository_document import CleanedRepositoryDocument
from document_categories.vectordb_document_categories.chunked_documents.repository_chunked_document import RepositoryChunkedDocument

from data_preprocessors.data_chunkers.base.data_chunker import DataChunker


class RepositoryDataChunker(DataChunker):
    post_chunk_cleaning=False

    @property
    def metadata(self) -> dict:
        _metadata={
            "chunk_size":150,
            "chunk_overlap":0,
            "minimum_chunk_size":50
        }

        return _metadata


    def chunk(self,cleaned_document:CleanedRepositoryDocument) -> list[RepositoryChunkedDocument]:
        cleaned_content=cleaned_document.content

        #Splitting Text:
        sentences=re.split("\n\n+",cleaned_content)

        chunked_sentences=[]

        maximum_chunk_size=self.metadata["chunk_size"]
        minimum_chunk_size=self.metadata["minimum_chunk_size"]
        chunk_overlap=self.metadata["chunk_overlap"]

        character_splitter=RecursiveCharacterTextSplitter(
            chunk_size=maximum_chunk_size,
            chunk_overlap=chunk_overlap
        )

        for sentence in sentences:
            if len(sentence)<maximum_chunk_size:
                if len(sentence)>=minimum_chunk_size:
                    chunked_sentences.append(sentence)

            else:
                splits=character_splitter.split_text(sentence)
                for split in splits:
                    if len(split)>=minimum_chunk_size:
                        chunked_sentences.append(split)


        if self.post_chunk_cleaning:
            cleaned_chunks=[
                self.clean_chunks(chunk=c)
                for c in chunked_sentences
            ]
            chunked_sentences=cleaned_chunks


        chunked_docs=[]
        for chunk in chunked_sentences:
            chunk_id=hashlib.md5(chunk.encode()).hexdigest()
            chunk_id=UUID(chunk_id,version=4)

            chunked_doc=RepositoryChunkedDocument(
                id=chunk_id,
                content=chunk,
                platform=cleaned_document.platform,
                document_id=cleaned_document.id,
                author_id=cleaned_document.author_id,
                author_full_name=cleaned_document.author_full_name,
                metadata=self.metadata,
                repository_name=cleaned_document.repository_name,
                link=cleaned_document.link,
                file_name=cleaned_document.file_name,
                programming_language_used=cleaned_document.programming_language_used
            )
            chunked_docs.append(chunked_doc)


        len_chunks=len(chunked_docs)
        file_name=cleaned_document.file_name
        repo_name=cleaned_document.repository_name

        logger.info(f"The cleaned file: {file_name} of repository: {repo_name} is chunked into {len_chunks} chunks.")

        return chunked_docs



