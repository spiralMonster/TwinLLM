import uuid
from loguru import logger

from abc import ABC
from typing import Generic,Type,TypeVar

from pydantic import UUID4,BaseModel,Field
from pymongo import errors

from databases.mongodb.mongodb_connection import connection
from settings import Settings


_database=connection.get_database(Settings.MONGODB_DATABASE_NAME)

T=TypeVar("T",bound="NoSQLBaseDocument")


class NoSQLBaseDocument(BaseModel,Generic[T],ABC):
    id: UUID4 = Field(default_factory=uuid.uuid4)

    class Settings:
        collection_name: str

    def __eq__(self,value:object) -> bool:
        if not isinstance(value,self.__class__):
            return False

        if self.id==value.id:
            return True

        else:
            return False


    def __hash__(self) -> int:
        h=hash(self.id)
        return h


    @classmethod
    def from_mongo(cls:Type[T],data:dict) -> T:
        if not data:
            raise ValueError("The data is empty!!!")

        id=data.pop("_id")

        inst=cls(**dict(data),id=id)

        return inst


    def model_dump(self: T, **kwargs) -> dict:
        dict_=super().model_dump(**kwargs)

        for key,value in dict_.items():
            if isinstance(value,uuid.UUID):
                dict_[key]=str(value)


        return dict_


    def to_mongo(self: T,**kwargs) -> dict:
        exclude_unset=kwargs.pop("exclude_unset",False)
        by_alias=kwargs.pop("by_alias",True)

        parsed=self.model_dump(
            exclude_unset=exclude_unset,
            by_alias=by_alias,
            **kwargs
        )

        if "_id" not in parsed and "id" in parsed:
            parsed["_id"]=str(parsed.pop("id"))


        for key, value in parsed.items():
            if isinstance(value,uuid.UUID):
                parsed[key]=str(value)


        return parsed


    @classmethod
    def get_collection_name(cls: Type[T]) -> str:
        if not hasattr(cls,"Settings") or not hasattr(cls.Settings,"collection_name"):
            raise ValueError(
                """
                Document should have a Settings configuration class.
                And also in that Settings class there should be a collection_name attribute
                """
            )


        collection_name=cls.Settings.collection_name

        return collection_name



    def save(self: T, **kwargs) -> T|None:
        collection_name=self.get_collection_name()
        collection=_database[collection_name]

        try:
            inst=self.to_mongo(**kwargs)
            collection.insert_one(inst)

            logger.info(f"Document with id: {self.id} inserted successfully.")

            return self

        except errors.WriteError:
            logger.exception("Failed to insert the document.")


        return None


    @classmethod
    def get_or_create(cls: Type[T],**filter_options) -> T:
        collection_name=cls.get_collection_name()
        collection=_database[collection_name]

        try:
            instance=collection.find_one(filter_options)
            if instance:
                obj=cls.from_mongo(instance)

                return obj

            new_instance=cls(**filter_options)
            new_instance=new_instance.save()

            return new_instance

        except errors.OperationFailure:
            logger.exception(
                f"Failed to retrieve the document with {filter_options}"
            )


    @classmethod
    def bulk_insert(cls:Type[T],documents:list[T],**kwargs) -> bool:
        collection_name=cls.get_collection_name()
        collection=_database[collection_name]

        try:
            docs_to_insert=[
                doc.to_mongo(**kwargs) for doc in documents
            ]

            collection.insert_many(docs_to_insert)
            return True

        except (errors.WriteError,errors.BulkWriteError):
            logger.error(f"Failed to insert the documents of class: {cls.__name__}")

        return False


    @classmethod
    def find(cls:Type[T],**filter_options) -> T|None:
        collection_name=cls.get_collection_name()
        collection=_database[collection_name]

        try:
            inst=collection.find_one(filter_options)
            if inst:
                obj=cls.from_mongo(inst)

                return obj

            return None

        except errors.OperationFailure:
            logger.error(f"Failed to find the document with document id: {cls.id} in collection: {cls.__name__}")
            return None


    @classmethod
    def bulk_find(cls:Type[T],**filter_options) -> list[T]:
        collection_name=cls.get_collection_name()
        collection=_database[collection_name]

        try:
            docs=[]

            instances=collection.find(filter_options)
            for inst in instances:
                if inst:
                    obj=cls.from_mongo(inst)
                    docs.append(obj)

            return docs

        except errors.OperationFailure:
            logger.error("Failed to retrieve the documents.")
            return []


    @classmethod
    def delete(cls: Type[T],**delete_options) -> bool:
        collection_name=cls.get_collection_name()
        collection=_database[collection_name]

        try:
            result=collection.delete_one(delete_options)

            if result:
                return True

        except errors.OperationFailure:
            logger.error(f"Failed to delete the instance from the collection: {cls.__name__}")

        return False


    @classmethod
    def bulk_delete(cls: Type[T],**delete_options) -> bool:
        collection_name=cls.get_collection_name()
        collection=_database[collection_name]

        try:
            result=collection.delete_many(delete_options)

            if result:
                return True

        except errors.OperationFailure:
            logger.error(f"Failed to delete the instances from collection: {cls.__name__}")


        return  False












