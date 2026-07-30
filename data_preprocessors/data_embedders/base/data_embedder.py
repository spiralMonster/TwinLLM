from abc import abstractmethod,ABC
from typing import Generic,TypeVar,cast

import string
from stop_words import get_stop_words

from document_categories.vectordb_document_categories.chunked_documents.base.chunked_document import ChunkedDocument
from document_categories.vectordb_document_categories.embedded_documents.base.embedded_document import EmbeddedDocument

from models.embedding_model import EmbeddingModel

ChunkedDocumentT=TypeVar("ChunkedDocumentT",bound=ChunkedDocument)
EmbeddedDocumentT=TypeVar("EmbeddedDocumentT",bound=EmbeddedDocument)

embedding_model=EmbeddingModel()


class DataEmbedder(ABC,Generic[ChunkedDocumentT,EmbeddedDocumentT]):
    pre_embedding_cleaning:bool=True

    @property
    def metadata(self) -> dict:
        _metadata={
            "embedding_model_id":embedding_model.model_id,
            "embedding_size":embedding_model.embedding_size,
            "max_input_lenght":embedding_model.max_input_length
        }

        return _metadata


    def clean_chunks(self,
                     chunk:str,
                     _ignore_punctuation_marks:list[str]=['<','>'],
                     _ignore_digits:list[str]=[],
                     convert_words_to_lowercase:bool=True,
                     remove_stopwords:bool=True
                     ) -> str:

        words=chunk.split(" ")

        punctuation_table=str.maketrans('','',string.punctuation)
        digit_table=str.maketrans('','',string.digits)

        stopwords=get_stop_words("english")

        cleaned_chunk=""
        for word in words:
            #Removing Punctuations:
            if not any(punctuation in word for punctuation in _ignore_punctuation_marks):
                word=word.translate(punctuation_table)

            #Removing Digits
            if not any(digit in word for digit in _ignore_digits):
                word=word.translate(digit_table)

            if word:
                #Transforming words into lower case:
                if convert_words_to_lowercase:
                    word=word.lower()

                #Removing Stopwords:
                if remove_stopwords:
                    if word not in stopwords:
                        cleaned_chunk+=word
                        cleaned_chunk+=" "

                    else:
                        pass

                else:
                    cleaned_chunk+=word
                    cleaned_chunk+=" "


        cleaned_chunk=cleaned_chunk.strip()

        return cleaned_chunk


    @abstractmethod
    def map_model(self,chunk:ChunkedDocumentT,embedding:list[float]) -> EmbeddedDocumentT:
        pass


    def embed_batch(self,chunked_data:list[ChunkedDocumentT]) -> list[EmbeddedDocumentT]:
        if self.pre_embedding_cleaning:
            embedding_model_input=[
                self.clean_chunks(
                    chunk=data.content
                )
                for data in chunked_data
            ]

        else:
            embedding_model_input=[
                data.content
                for data in chunked_data
            ]

        embeddings=embedding_model(
            input_text=embedding_model_input,
            to_list=True
        )
        final_embeddings=[
            cast(list[float],embed)
            for embed in embeddings
        ]

        result=[
            self.map_model(chunk=chunk,embedding=embedding)
            for chunk,embedding in zip(chunked_data,final_embeddings)
        ]

        return result



    def embed(self,chunk:ChunkedDocumentT) -> EmbeddedDocumentT:
        embed_data=self.embed_batch(
            chunked_data=[chunk]
        )[0]

        return embed_data
