from abc import abstractmethod,ABC
from langchain_core.prompts import ChatPromptTemplate


class PromptTemplateFactory(ABC):
    @staticmethod
    @abstractmethod
    def create_prompt() -> ChatPromptTemplate:
        pass