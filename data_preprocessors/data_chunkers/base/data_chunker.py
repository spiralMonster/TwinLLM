import string
from stop_words import get_stop_words

from abc import ABC,abstractmethod
from typing import Generic,TypeVar

from document_categories.vectordb_document_categories.cleaned_documents.base.cleaned_document import CleanedDocument
from document_categories.vectordb_document_categories.chunked_documents.base.chunked_document import ChunkedDocument


CleanedDocumentT=TypeVar("CleanedDocumentT",bound=CleanedDocument)
ChunkedDocumentT=TypeVar("ChunkedDocumentT",bound=ChunkedDocument)


class DataChunker(ABC,Generic[CleanedDocumentT,ChunkedDocumentT]):
    post_chunk_cleaning: bool


    @property
    def metadata(self) ->dict:
        _metadata={
            "chunk_size":150,
            "chunk_overlap":20,
            "minimum_chunk_size":30
        }

        return _metadata


    @abstractmethod
    def chunk(self,cleaned_document:CleanedDocumentT) ->list[ChunkedDocumentT]:
        pass


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
