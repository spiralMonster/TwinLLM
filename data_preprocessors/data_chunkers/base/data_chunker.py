import string
from stop_words import get_stop_words

from abc import ABC,abstractmethod
from typing import Generic,TypeVar

from document_categories.vectordb_document_categories.cleaned_documents.base.cleaned_document import CleanedDocument
from document_categories.vectordb_document_categories.chunked_documents.base.chunked_document import ChunkedDocument


CleanedDocumentT=TypeVar("CleanedDocumentT",bound=CleanedDocument)
ChunkedDocumentT=TypeVar("ChunkedDocumentT",bound=ChunkedDocument)


class DataChunker(ABC,Generic[CleanedDocumentT,ChunkedDocumentT]):
    @property
    def metadata(self) ->dict:
        _metadata={
            "maximum_chunk_size":500,
            "chunk_overlap":150,
            "minimum_chunk_size":80
        }

        return _metadata


    @abstractmethod
    def chunk(self,cleaned_document:CleanedDocumentT) ->list[ChunkedDocumentT]:
        pass



    def _chunk(
            self,
            sentences:list[str],
            min_chunk_length:int,
            max_chunk_length:int,
            chunk_overlap:int
    )-> list[str]:

        extracts=[]
        current_chunk=""
        for sentence in sentences:
            if len(current_chunk)+len(sentence)<=max_chunk_length:
                current_chunk+=sentence+" "

            else:
                if len(current_chunk)>=min_chunk_length:
                    if extracts:
                        prev_chunk=extracts[-1]
                        prev_chunk_tokens=prev_chunk.split(" ")

                        chunk_overlap_in_tokens=chunk_overlap//5
                        if len(prev_chunk_tokens)>chunk_overlap_in_tokens:
                            overlap_words=prev_chunk_tokens[-chunk_overlap_in_tokens:]

                        else:
                            overlap_words=prev_chunk_tokens

                        overlap_text=" ".join(overlap_words).strip()

                        final_chunk=overlap_text+" "+current_chunk
                        final_chunk=final_chunk.strip()



                    else:
                        final_chunk=current_chunk.strip()

                    extracts.append(final_chunk)

                current_chunk=sentence+" "

        if len(current_chunk)>=min_chunk_length:
            if extracts:
                prev_chunk=extracts[-1]
                final_chunk=prev_chunk[-chunk_overlap:]+" "+current_chunk
                final_chunk=final_chunk.strip()

                extracts.append(final_chunk)


        return extracts

