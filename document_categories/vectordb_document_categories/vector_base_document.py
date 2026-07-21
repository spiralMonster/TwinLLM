import uuid
from uuid import UUID
from abc import ABC
from typing import Any, Generic,Type,TypeVar,Callable,Dict

from loguru import logger
from pydantic import BaseModel,Field,UUID4
import numpy as np

from qdrant_client.http import exceptions
from qdrant_client.http.models import Distance,VectorParams
from qdrant_client.models import PointStruct,CollectionInfo,Record

from databases.qdrant.qdrant_connection import connection
from document_categories.data_category import DataCategory

from utils.exceptions.qdrant_exceptions.improperly_configured_exception import ImproperlyConfiguredException
from utils.exceptions.qdrant_exceptions.collection_creation_exception import CollectionCreationException
from utils.exceptions.qdrant_exceptions.document_insertion_exception import DocumentInsertionException
from utils.exceptions.qdrant_exceptions.find_document_exception import FindDocumentException
from utils.exceptions.qdrant_exceptions.search_exception import SearchException

from models.embedding_model import EmbeddingModel

T=TypeVar("T",bound="VectorBaseDocument")


class VectorBaseDocument(BaseModel,Generic[T],ABC):
    id: UUID4 = Field(default_factory=uuid.uuid4)

    class Config:
        category: str
        collection_name: str
        use_vector_index: bool


    def __eq__(self,value:object) -> bool:
        if not isinstance(value,self.__class__):
            return False

        else:
            if self.id==value.id:
                return True

            else:
                return False


    def __hash__(self) -> int:
        hash_val=hash(self.id)

        return hash_val


    @classmethod
    def _has_class_attribute(cls:Type[T],attribute_name:str) -> bool:
        if attribute_name in cls.__annotations__:
            return True

        for base in cls.__bases__:
            if hasattr(base,"_has_class_attribute") and base._has_class_attribute(attribute_name):
                return True

        return False



    @classmethod
    def from_record(cls: Type[T],point:Record) -> T:
        _id=UUID(str(point.id),version=4)

        if point.payload:
            pay_load=point.payload

        else:
            pay_load={}


        attributes={
            "id":_id,
            **pay_load
        }

        if cls._has_class_attribute("embedding"):
            if point.vector:
                attributes["embedding"]=point.vector

            else:
                attributes["embedding"]=None


        return cls(**attributes)



    def __uuid_to_str(self,item:Any) -> Any:
        if isinstance(item,UUID):
            return str(item)


        else:
            if isinstance(item,dict):
                for key,value in item.items():
                    if isinstance(value,UUID):
                        item[key]=str(value)

                    elif isinstance(value,list):
                        item[key]=[self.__uuid_to_str(v) for v in value]

                    elif isinstance(value,dict):
                        item[key]={k:self.__uuid_to_str(v) for k,v in value.items()}

            return item


    def model_dump(self:T,**kwargs) -> dict:
        dict_=super().model_dump(**kwargs)
        dict_=self.__uuid_to_str(dict_)

        return dict_



    def to_point(self:T,**kwargs) -> PointStruct:
        exclude_unset=kwargs.pop("exclude_unset",False)
        by_alias=kwargs.pop("by_alias",True)

        pay_load=self.model_dump(
            exclude_unset=exclude_unset,
            by_alias=by_alias,
            **kwargs
        )

        _id=str(pay_load.pop("id"))
        vector=pay_load.pop("embedding",{})
        if vector and isinstance(vector,np.ndarray):
            vector=vector.tolist()


        point=PointStruct(
            id=_id,
            vector=vector,
            payload=pay_load
        )

        return point


    @classmethod
    def get_collection_name(cls: Type[T]) -> str:
        if not hasattr(cls,"Config") or not hasattr(cls.Config,"collection_name"):
            logger.error("Couldn't find the Config class.")
            logger.error("Couldn't find the 'collection_name' attribute in Config class.")

            raise ImproperlyConfiguredException(
                "Class should contain the Config class with 'collection_name' attribute."
            )

        else:
            collection_name=cls.Config.collection_name

            return collection_name


    @classmethod
    def get_use_vector_index(cls:Type[T]) -> bool:
        if not hasattr(cls,"Config") or not hasattr(cls.Config,"use_vector_index"):
            logger.error("Couldn't find the Config class.")
            logger.error("Couldn't find the 'use_vector_index' attribute in Config class.")

            raise ImproperlyConfiguredException(
                "Class should contain the Config class with 'use_vector_index' attribute."
            )

        else:
            use_vector_index=cls.Config.use_vector_index
            return use_vector_index


    @classmethod
    def _create_collection(cls:Type[T],collection_name:str,use_vector_index:bool) -> bool:
        if use_vector_index:
            vector_config=VectorParams(
                size=EmbeddingModel().embedding_size,
                distance=Distance.COSINE
            )

        else:
            vector_config={}


        result=connection.create_collection(
            collection_name=collection_name,
            vectors_config=vector_config
        )

        return result


    @classmethod
    def create_collection(cls:Type[T]) -> bool:
        collection_name=cls.get_collection_name()
        use_vector_index=cls.get_use_vector_index()

        result=cls._create_collection(
            collection_name=collection_name,
            use_vector_index=use_vector_index
        )

        return result


    @classmethod
    def get_or_create_collection(cls: Type[T]) -> CollectionInfo:
        collection_name=cls.get_collection_name()
        try:
            collection_info=connection.get_collection(collection_name=collection_name)


        except exceptions.UnexpectedResponse:
            logger.info("Collection doesn't exist.")
            logger.info("Creating collection...")

            use_vector_index=cls.get_use_vector_index()
            collection_created=cls._create_collection(
                collection_name=collection_name,
                use_vector_index=use_vector_index
            )

            if not collection_created:
                logger.error("Error in creating collection")

                raise CollectionCreationException("Failed to create the collection in Qdrant Database")


            collection_info=connection.get_collection(collection_name=collection_name)


        return collection_info


    @classmethod
    def _bulk_insert(cls:Type[T],documents:list["VectorBaseDocument"]) -> None:
        collection_name=cls.get_collection_name()
        points=[doc.to_point() for doc in documents]

        connection.upsert(
            collection_name=collection_name,
            points=points
        )


    @classmethod
    def bulk_insert(cls:Type[T],documents:list["VectorBaseDocument"]) -> bool:
        try:
            cls._bulk_insert(documents=documents)


        except exceptions.UnexpectedResponse:
            collection_name=cls.get_collection_name()
            logger.info(f"Collection name: {collection_name} does not exist. Creating the collection and then inserting the documents.")

            cls.create_collection()
            try:
                cls._bulk_insert(documents=documents)

            except exceptions.UnexpectedResponse:
                logger.error("Failed to insert the document.")

                raise DocumentInsertionException("Failed to insert the documents in Qdrant Database.")

            return True

        return True


    @classmethod
    def _bulk_find(cls: Type[T],limit:int=10,**kwargs) -> tuple[UUID|None,list[T]]:
        collection_name=cls.get_collection_name()

        offset=kwargs.pop("offset",None)
        offset=str(offset) if offset else None

        with_payload=kwargs.pop("with_payload",True)
        with_vectors=kwargs.pop("with_vectors",False)

        records,next_offset=connection.scroll(
            collection_name=collection_name,
            limit=limit,
            with_payload=with_payload,
            with_vectors=with_vectors,
            offset=offset,
            **kwargs
        )

        documents=[cls.from_record(record) for record in records]

        if not next_offset:
            next_offset=UUID(next_offset,version=4)


        return next_offset,documents


    @classmethod
    def bulk_find(cls:Type[T],limit:int=10,**kwargs) -> tuple[UUID|None,list[T]]:
        try:
            next_offset,documents=cls._bulk_find(limit=limit,**kwargs)
            return next_offset,documents

        except exceptions.UnexpectedResponse:
            collection_name=cls.get_collection_name()
            logger.error(f"Failed to find the documents in: {collection_name}")

            raise FindDocumentException("Failed to find the documents in Qdrant Database.")



    @classmethod
    def _search(cls:Type[T],query_vector:list,limit:int=10,**kwargs) -> list[T]:
        collection_name=cls.get_collection_name()

        with_payload=kwargs.pop("with_payload",True)
        with_vectors=kwargs.pop("with_vectors",False)

        records=connection.search(
            collection_name=collection_name,
            query_vector=query_vector,
            limit=limit,
            with_payload=with_payload,
            with_vectors=with_vectors,
            **kwargs
        )

        documents=[cls.from_record(record) for record in records]

        return documents


    @classmethod
    def search(cls:Type[T],query_vector:list,limit:int=10,**kwargs) -> list[T]:
        try:
            documents=cls._search(
                query_vector=query_vector,
                limit=limit,
                **kwargs
            )

            return documents

        except exceptions.UnexpectedResponse:
            logger.error(f"Failed to search for the given query.")

            raise SearchException("Failed to search for the given query in Qdrant Vector Database.")



    @classmethod
    def get_category(cls: Type[T]) -> str:
        if not hasattr(cls,"Config") or not hasattr(cls.Config,"category"):
            logger.error("Couldn't find the Config class.")
            logger.error("Couldn't find the 'category' attribute in Config class.")

            raise ImproperlyConfiguredException(
                "Class should contain the Config class with 'category' attribute."
            )

        else:
            category=cls.Config.category
            return category



    @classmethod
    def _group_by(cls:Type[T],documents:list[T],selector:Callable[[T],Any]) -> Dict[Any,list[T]]:
        grouped={}

        for doc in documents:
            key=selector(doc)
            if key not in grouped:
                grouped[key]=[]

            grouped[key].append(doc)

        return grouped


    @classmethod
    def group_by_category(cls:Type[T],documents:list[T]) -> Dict[DataCategory,list[T]]:
        selector=lambda doc: doc.get_category()

        result=cls._group_by(documents=documents,selector=selector)
        return result


    @classmethod
    def group_by_class(
            cls:Type["VectorBaseDocument"],
            documents:list["VectorBaseDocument"]
    ) -> Dict["VectorBaseDocument",list["VectorBaseDocument"]]:

        selector=lambda doc: doc.__class__

        result=cls._group_by(documents=documents,selector=selector)
        return result


    @classmethod
    def collection_name_to_class(cls:Type["VectorBaseDocument"],collection_name:str) -> type["VectorBaseDocument"]:
        for subclass in cls.__subclasses__():
            try:
                if subclass.get_collection_name()==collection_name:
                    return subclass

            except ImproperlyConfiguredException:
                pass

            try:
                return subclass.collection_name_to_class(collection_name=collection_name)

            except ValueError:
                continue


        raise ValueError(f"No subclass found for collection name: {collection_name}")





























