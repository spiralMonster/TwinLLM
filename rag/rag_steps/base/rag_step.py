from abc import abstractmethod,ABC
from typing import Any

from document_categories.rag_document_categories.query_document import Query

from langchain.chat_models import BaseChatModel
from langchain_mistralai import ChatMistralAI

from settings import Settings


class RagStep(ABC):
    model:BaseChatModel=ChatMistralAI(
        api_key=Settings.RAG_MODEL_API_KEY,
        model_name=Settings.RAG_MODEL_NAME,
        temperature=Settings.RAG_MODEL_TEMPERATURE,
        max_retries=Settings.RAG_MODEL_MAX_RETRIES
    )


    @abstractmethod
    def generate(self,query:Query,*args,**kwargs) -> Any:
        pass