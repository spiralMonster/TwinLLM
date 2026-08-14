from abc import abstractmethod,ABC
from typing import Generic,TypeVar

from document_categories.vectordb_document_categories.embedded_documents.base.embedded_document import EmbeddedDocument

EmbeddedDocumentT=TypeVar("EmbeddedDocumentT",bound=EmbeddedDocument)

class CraftPrompt(ABC,Generic[EmbeddedDocumentT]):
    @staticmethod
    @abstractmethod
    def craft_prompt(documents:list[EmbeddedDocumentT]) -> str:
        pass