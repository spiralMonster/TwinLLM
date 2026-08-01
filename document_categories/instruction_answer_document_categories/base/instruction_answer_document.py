from abc import ABC
from pydantic import BaseModel
from typing import Type,TypeVar,Generic
from loguru import logger

from utils.exceptions.general_exceptions.improperly_configured_exception import ImproperlyConfiguredException


T=TypeVar("T",bound="InstructionAnswerDocument")


class InstructionAnswerDocument(BaseModel,Generic[T],ABC):
    instruction:str
    answer:str
    
    class Config:
        data_category:str
    
    
    @classmethod
    def get_category(cls:Type[T]) -> str:
        if not hasattr(cls,"Config") or not hasattr(cls.Config,"data_category"):
            logger.error("Couldn't find the Config class.")
            logger.error("Couldn't find the 'data_category' attribute in Config class.")

            raise ImproperlyConfiguredException(
                "Class should contain the Config class with 'data_category' attribute."
            )


        else:
            category=cls.Config.data_category
            return category
            


