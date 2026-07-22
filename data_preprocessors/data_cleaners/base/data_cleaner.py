import re
import unicodedata
from urllib.parse import urlparse
from abc import ABC,abstractmethod
from typing import Generic,TypeVar

from document_categories.nosql_db_document_categories.base.base_document import Document
from document_categories.vectordb_document_categories.cleaned_documents.base.cleaned_document import CleanedDocument


DocumentT=TypeVar("DocumentT",bound=Document)
CleanedDocumentT=TypeVar("CleanedDocumentT",bound=CleanedDocument)



class DataCleaner(ABC,Generic[DocumentT,CleanedDocumentT]):
    def remove_extra_spaces(self,text:str) -> str:
        cleaned_content=re.sub(r"\s+"," ",text)
        return cleaned_content


    def remove_or_replace_url(self,text:str,replace_with:str) -> str:
        cleaned_content=re.sub(r"https?://[^\s]+",replace_with,text)
        return cleaned_content


    def is_valid_date(self,date:str) -> bool:
        if re.match(
            r"^\d{4}-(0[1-9]|1[0-2])-(0[1-9]|1[0-9]|2[0-9]|3[01])$",
            date

        ):
            return True

        elif re.match(
            r"^[A-Z]{3}\s(0[1-9]|1[0-9]|2[0-9]|3[0-1]),\s\d{4}$",
            date
        ):
            return True

        elif re.match(
            r"^[A-Z][a-z]{2}\s(0[1-9]|1[0-9]|2[0-9]|3[0-1]),\s\d{4}$",
            date
        ):
            return True

        elif re.match(
            r"^[A-Za-z]+,\s[A-Za-z]+\s([1-9]|1[0-9]|2[0-9]|3[0-1]),\s\d{4}\sat\s([1-9]|1[0-2]):\d{2}\s(PM|AM)$",
            date
        ):
            return True

        else:
            return False


    def is_valid_link(self,link:str,domains:list[str]) -> bool:
        for domain in domains:
            domain=urlparse(domain).netloc
            pattern=rf"https://([a-zA-Z0-9-]+\.)?{re.escape(domain)}(/.*)?$"

            if re.match(pattern,link):
                return True


        return False


    def remove_or_replace_non_ascii_characters(self,text:str,replace_with:str|None) -> str:
        text=text.strip()
        cleaned_words=[]

        for ch in text:
            if unicodedata.category(ch)[0] in {"L","N","P","Z"}:
                cleaned_words.append(ch)

            else:
                if replace_with:
                    cleaned_words.append(replace_with)


        cleaned_text="".join(cleaned_words)
        cleaned_text=cleaned_text.strip()

        return cleaned_text


    def get_content_length(self,content:str) -> int:
        words=content.split(" ")
        len_content=len(words)

        return len_content



    @abstractmethod
    def clean(self,document_model:DocumentT,min_content_length:int) -> CleanedDocumentT|list[CleanedDocumentT]|None:
        pass

