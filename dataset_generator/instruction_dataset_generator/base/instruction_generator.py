from concurrent.futures import as_completed,ThreadPoolExecutor
from tqdm.auto import tqdm

from abc import abstractmethod,ABC
from typing import TypeVar,Generic
from pydantic import SecretStr
from loguru import logger

from langchain_core.prompts import ChatPromptTemplate
from langchain.chat_models import BaseChatModel


from langchain_mistralai import ChatMistralAI
from langchain_cohere import ChatCohere
from langchain_groq import ChatGroq
from langchain_qwq import ChatQwen

from document_categories.vectordb_document_categories.chunked_documents.base.chunked_document import ChunkedDocument
from document_categories.instruction_answer_document_categories.base.instruction_answer_document import InstructionAnswerDocument
from dataset_generator.instruction_dataset_generator.utils.instruction_dataset_generator_specs import InstructionDatasetGeneratorSpecs

from utils.batch_data import batch
from settings import Settings


ChunkedDocumentT=TypeVar("ChunkedDocumentT",bound=ChunkedDocument)
InstructionAnswerDocumentT=TypeVar("InstructionAnswerDocumentT",bound=InstructionAnswerDocument)


class InstructionGenerator(ABC,Generic[ChunkedDocumentT,InstructionAnswerDocumentT]):
    MODEL_TEMPERATURE:float=Settings.INSTRUCT_ANS_GENERATOR_TEMP
    MODEL_MAX_RETRIES:int=Settings.INSTRUCT_ANS_GENERATOR_MAX_RETRIES

    @staticmethod
    def initialize_mistral_model(api_key:SecretStr,temperature:float,max_retries:int=3) -> BaseChatModel:
        model=ChatMistralAI(
            api_key=api_key,
            model_name=Settings.MISTRAL_MODEL,
            temperature=temperature,
            max_retries=max_retries
        )

        return model

    @staticmethod
    def initialize_cohere_model(api_key:SecretStr,temperature:float,max_retries:int=3) -> BaseChatModel:
        model=ChatCohere(
            cohere_api_key=api_key,
            model=Settings.COHERE_MODEL,
            temperature=temperature,
            max_retries=max_retries
        )

        return model

    @staticmethod
    def initialize_groq_model(api_key:SecretStr,temperature:float,max_retries:int=3) -> BaseChatModel:
        model=ChatGroq(
            api_key=api_key,
            model=Settings.GROQ_MODEL,
            temperature=temperature,
            max_retries=max_retries
        )

        return model

    @staticmethod
    def initialize_qwen_model(api_key:SecretStr,temperature:float,max_retries:int=3) -> BaseChatModel:
        model=ChatQwen(
            api_key=api_key,
            model=Settings.QWEN_MODEL,
            temperature=temperature,
            max_retries=max_retries
        )

        return model


    @staticmethod
    def generate_prompt() -> ChatPromptTemplate:
        prompt_template="""
        You are an Instruction Dataset Curator.
        You are given some {data_type} data chunks along with it's metadata.
        Your job is to generate a pair of instruction and answer for every data chunk.
        
        # Things to remember while generating the instruction-answer pair:
          - Each instruction must ask to write about a specific topic contained in the data chunk.
          - Only use the concepts from the data chunk to generate instruction.
          - Instructions must be self-contained and general.
          - Each answer must provide a relevant paragraph based on the information found in the data chunk.
          - Answers must imitate the writing style of the data chunk.
        
        # Data Chunks:
        {data_chunks}
        """

        prompt=ChatPromptTemplate.from_template(
            template=prompt_template,
            input_variable=["data_type","data_chunks"]
        )

        return prompt



    @staticmethod
    def generate_instruction_answer_pair(
            data_type:str,
            data_chunks:str,
            prompt:ChatPromptTemplate,
            model:BaseChatModel
    ) -> tuple[list[str],list[str]]:

        model=model.with_structured_output(InstructionDatasetGeneratorSpecs)
        generation_chain=prompt|model

        try:
            response=generation_chain.invoke(
                {
                    "data_type":data_type,
                    "data_chunks":data_chunks
                }
            )

            if not isinstance(response,InstructionDatasetGeneratorSpecs):
                logger.info("[Warning]: The model generated the invalid response!!!")
                return [],[]

            else:
                instructions=[]
                answers=[]

                for pair in response.instruction_answer_pair:
                    instructions.append(pair.instruction)
                    answers.append(pair.answer)


                return instructions,answers

        except Exception as e:
            logger.info(f"Exception Encountered: {e}")

            return [],[]


    @abstractmethod
    def create_data_chunks(self,chunks:list[ChunkedDocumentT]) -> list[str]:
        pass


    @staticmethod
    def join_data_chunks(data_chunks:list[str]) ->str:
        chunk="\n\n".join(data_chunks)
        chunk=chunk.strip("\n")
        return chunk


    def generate_instruction_answer_dataset(
            self,
            models:list[BaseChatModel],
            data_type:str,
            data_chunks:list[str],
            data_chunks_per_prompt:int=3,
    ) -> tuple[list,list]:

        instructions=[]
        answers=[]

        model_prompt=self.generate_prompt()

        chunk_batches=batch(data_chunks,batch_size=data_chunks_per_prompt)
        for chunk_batch in tqdm(chunk_batches,total=len(chunk_batches)):
            data_chunk=self.join_data_chunks(data_chunks=chunk_batch)

            with ThreadPoolExecutor() as executor:
                futures=[
                    executor.submit(
                        self.generate_instruction_answer_pair,
                        data_type,
                        data_chunk,
                        model_prompt,
                        model
                    )
                    for model in models
                ]

                for future in as_completed(futures):
                    instruct,ans=future.result()
                    instructions.extend(instruct)
                    answers.extend(ans)


        return instructions,answers




    @abstractmethod
    def generate(self,chunked_documents:list[ChunkedDocumentT]) -> list[InstructionAnswerDocumentT]:
        pass


    @staticmethod
    def llm_models_used() -> list[str]:
        models_used=[
            Settings.MISTRAL_MODEL,
            Settings.COHERE_MODEL,
            Settings.GROQ_MODEL,
            Settings.QWEN_MODEL
        ]

        return models_used




