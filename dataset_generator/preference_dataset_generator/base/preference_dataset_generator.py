from abc import abstractmethod,ABC
from typing import TypeVar,Generic
from pydantic import SecretStr
from loguru import logger

from concurrent.futures import as_completed,ThreadPoolExecutor
from tqdm.auto import tqdm

from langchain_core.prompts import ChatPromptTemplate
from langchain.chat_models import BaseChatModel

from langchain_mistralai import ChatMistralAI
from langchain_cohere import ChatCohere
from langchain_groq import ChatGroq
from langchain_qwq import ChatQwen

from document_categories.vectordb_document_categories.chunked_documents.base.chunked_document import ChunkedDocument
from document_categories.preference_dataset_document_categories.base.preference_document import PreferenceDocument

from dataset_generator.preference_dataset_generator.utils.preference_dataset_generator_specs import PreferenceDatasetGeneratorSpecs

from utils.batch_data import batch
from settings import Settings


ChunkedDocumentT=TypeVar("ChunkedDocumentT",bound=ChunkedDocument)
PreferenceDocumentT=TypeVar("PreferenceDocumentT",bound=PreferenceDocument)


class PreferenceDatasetGenerator(ABC,Generic[ChunkedDocumentT,PreferenceDocumentT]):
    @staticmethod
    def initialize_mistral_model(
            api_key:SecretStr,
            temperature:float,
            max_retries:int=3
    ) -> BaseChatModel:
        model=ChatMistralAI(
            api_key=api_key,
            model_name=Settings.MISTRAL_MODEL_FOR_PREFERENCE_DATASET_GEN,
            temperature=temperature,
            max_retries=max_retries
        )

        return model

    @staticmethod
    def initialize_cohere_model(
            api_key:SecretStr,
            temperature:float,
            max_retries:int=3
    ) -> BaseChatModel:
        model=ChatCohere(
            cohere_api_key=api_key,
            model=Settings.COHERE_MODEL_FOR_PREFERENCE_DATASET_GEN,
            temperature=temperature,
            max_retries=max_retries
        )

        return model

    @staticmethod
    def initialize_groq_model(
            api_key:SecretStr,
            temperature:float,
            max_retries:int=3
    ) -> BaseChatModel:
        model=ChatGroq(
            api_key=api_key,
            model=Settings.GROQ_MODEL_FOR_PREFERENCE_DATASET_GEN,
            temperature=temperature,
            max_retries=max_retries
        )

        return model

    @staticmethod
    def initialize_qwen_model(
            api_key:SecretStr,
            temperature:float,
            max_retries:int=3
    ) -> BaseChatModel:
        model=ChatQwen(
            api_key=api_key,
            model=Settings.GWEN_MODEL_FOR_PREFERENCE_DATASET_GEN,
            temperature=temperature,
            max_retries=max_retries
        )

        return model


    @staticmethod
    def get_llm_models_used() -> list[str]:
        models_used=[
            Settings.MISTRAL_MODEL_FOR_PREFERENCE_DATASET_GEN,
            Settings.COHERE_MODEL_FOR_PREFERENCE_DATASET_GEN,
            Settings.GROQ_MODEL_FOR_PREFERENCE_DATASET_GEN,
            Settings.GWEN_MODEL_FOR_PREFERENCE_DATASET_GEN
        ]

        return models_used


    @staticmethod
    def generate_prompt() -> ChatPromptTemplate:
        template="""
        You are a Preference Dataset Curator.
        You are provided with some {data_type} data chunks.
        Your job is to generate a triplet of instruction,chosen answer and rejected answer for each data chunk.
        
        # Things to remember while generating the triplet:
          - Each instruction must ask to write about a specific topic contained in the data chunk.
          - Only use the concepts from the data chunk to generate instruction.
          - Instructions must be self contained and general.
          - Each chosen answer must imitate the writing style of the data chunk,so that it seems to be written by the author of data chunk.
          - Each rejected answer should be more of a general way of answering the instruction, without imitating any writing style of data chunk.
        
        # Data Chunks:
        {data_chunks}
        """

        prompt=ChatPromptTemplate.from_template(
            template=template,
            input_variable=["data_type","data_chunks"]
        )

        return prompt


    @staticmethod
    def generate_preference_triplet(
            data_type:str,
            data_chunks:str,
            prompt:ChatPromptTemplate,
            model:BaseChatModel
    ) -> tuple[list[str],list[str],list[str]]:

        model=model.with_structured_output(
            PreferenceDatasetGeneratorSpecs
        )
        generation_chain=prompt|model

        try:
            response=generation_chain.invoke(
                {
                    "data_type":data_type,
                    "data_chunks":data_chunks
                }
            )

            if not isinstance(response,PreferenceDatasetGeneratorSpecs):
                logger.info("[Warning]: The model generated the invalid response!!!")

                return [],[],[]

            else:
                instructions=[]
                chosen_answers=[]
                rejected_answers=[]

                for triplet in response.triplets:
                    instructions.append(triplet.instruction)
                    chosen_answers.append(triplet.chosen_answer)
                    rejected_answers.append(triplet.rejected_answer)


                return instructions,chosen_answers,rejected_answers

        except Exception as e:
            logger.info(f"Exception encountered: {e}")

            return [],[],[]


    @staticmethod
    def join_data_chunks(data_chunks:list[str]) -> str:
        chunk="\n\n".join(data_chunks)
        chunk=chunk.strip("\n")

        return chunk



    def generate_preference_dataset(
            self,
            models:list[BaseChatModel],
            data_type:str,
            data_chunks:list[str],
            data_chunks_per_prompt:int=3
    ) -> tuple[list,list,list]:

        instructions=[]
        chosen_answers=[]
        rejected_answers=[]

        prompt=self.generate_prompt()

        chunk_batches=batch(data_chunks,batch_size=data_chunks_per_prompt)
        for chunk_batch in tqdm(chunk_batches,total=len(chunk_batches)):
            data_chunk=self.join_data_chunks(data_chunks=chunk_batch)

            with ThreadPoolExecutor() as executor:
                futures=[
                    executor.submit(
                        self.generate_preference_triplet,
                        data_type,
                        data_chunk,
                        prompt,
                        model
                    )
                    for model in models
                ]

                for future in as_completed(futures):
                    instruct,chosen_ans,rejected_ans=future.result()

                    instructions.extend(instruct)
                    chosen_answers.extend(chosen_ans)
                    rejected_answers.extend(rejected_ans)


        return instructions,chosen_answers,rejected_answers


    @abstractmethod
    def generate(self,chunked_documents:list[ChunkedDocumentT]) -> list[PreferenceDocumentT]:
        pass





