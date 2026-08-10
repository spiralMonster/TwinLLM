from abc import ABC
from typing import Generic,TypeVar,Type
from pydantic import BaseModel
from loguru import logger

from utils.exceptions.general_exceptions.improperly_configured_exception import ImproperlyConfiguredException

T=TypeVar("T",bound="PreferenceDocument")


class PreferenceDocument(BaseModel,Generic[T],ABC):
    instruction:str
    chosen_answer:str
    rejected_answer:str

    class Config:
        data_category:str


    @classmethod
    def get_category(cls:Type[T]) -> str:
        if not hasattr(cls,"Config") or not hasattr(cls.Config,"data_category"):
            logger.error("Couldn't find the Config class.")
            logger.error("Couldn't find the 'data_category' attribute in Config class.")

            raise ImproperlyConfiguredException("Class should contain the Config class with 'data_category' attribute.")

        else:
            data_cat=cls.Config.data_category
            return data_cat