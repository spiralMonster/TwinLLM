import time
from concurrent.futures import as_completed,ThreadPoolExecutor
from tqdm.auto import tqdm

from abc import abstractmethod,ABC
from typing import TypeVar,Generic
from loguru import logger

from langchain_core.prompts import ChatPromptTemplate
from langchain.chat_models import BaseChatModel

from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_mistralai import ChatMistralAI
from langchain_anthropic import ChatAnthropic
from langchain_cohere import ChatCohere
from langchain_deepseek import ChatDeepSeek
from langchain_groq import ChatGroq
from langchain_perplexity import ChatPerplexity

from document_categories.vectordb_document_categories.chunked_documents.base.chunked_document import ChunkedDocument
from dataset_generator.instruction_dataset_generator.utils.instruction_dataset_generator_specs import InstructionDatasetGeneratorSpecs

from utils.batch_data import batch
from settings import Settings


ChunkedDocumentT=TypeVar("ChunkedDocumentT",bound=ChunkedDocument)


class InstructionGenerator(ABC,Generic[ChunkedDocumentT]):
    @staticmethod
    def initialize_gpt_model(temperature:float,max_retries:int=3) -> BaseChatModel:
        model=ChatOpenAI(
            api_key=Settings.OPENAI_API_KEY,
            temperature=temperature,
            max_retries=max_retries
        )

        return model

    @staticmethod
    def initialize_gemini_model(temperature:float,max_retries:int=3) -> BaseChatModel:
        model=ChatGoogleGenerativeAI(
            api_key=Settings.GEMINI_API_KEY,
            temperature=temperature,
            max_retries=max_retries
        )

        return model

    @staticmethod
    def initialize_mistral_model(temperature:float,max_retries:int=3) -> BaseChatModel:
        model=ChatMistralAI(
            api_key=Settings.MISTRAL_API_KEY,
            temperature=temperature,
            max_retries=max_retries
        )

        return model

    @staticmethod
    def initialize_anthropic_model(temperature:float,max_retries:int=3) -> BaseChatModel:
        model=ChatAnthropic(
            api_key=Settings.ANTHROPIC_API_KEY,
            temperature=temperature,
            max_retries=max_retries
        )

        return model

    @staticmethod
    def initialize_cohere_model(temperature:float) -> BaseChatModel:
        model=ChatCohere(
            cohere_api_key=Settings.COHERE_API_KEY,
            temperature=temperature
        )

        return model

    @staticmethod
    def initialize_deepseek_model(temperature:float,max_retries:int=3) -> BaseChatModel:
        model=ChatDeepSeek(
            api_key=Settings.DEEPSEEK_API_KEY,
            temperature=temperature,
            max_retries=max_retries
        )

        return model

    @staticmethod
    def initialize_groq_model(temperature:float,max_retries:int=3) -> BaseChatModel:
        model=ChatGroq(
            api_key=Settings.GROQ_API_KEY,
            temperature=temperature,
            max_retries=max_retries
        )

        return model

    @staticmethod
    def initialize_perplexity_model(temperature:float,max_retries:int=3) -> BaseChatModel:
        model=ChatPerplexity(
            api_key=Settings.PERPLEXITY_API_KEY,
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
            time.sleep(5)
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
            data_type:str,
            data_chunks:list[str],
            data_chunks_per_prompt:int=3,
            model_temperature:float=0.6
    ) -> tuple[list,list]:

        instructions=[]
        answers=[]

        model_gpt=self.initialize_gpt_model(temperature=model_temperature)
        model_gemini=self.initialize_gemini_model(temperature=model_temperature)
        model_mistral=self.initialize_mistral_model(temperature=model_temperature)
        model_anthropic=self.initialize_anthropic_model(temperature=model_temperature)
        model_cohere=self.initialize_cohere_model(temperature=model_temperature)
        model_groq=self.initialize_groq_model(temperature=model_temperature)
        model_perplexity=self.initialize_perplexity_model(temperature=model_temperature)
        model_deepseek=self.initialize_deepseek_model(temperature=model_temperature)
        
        model_prompt=self.generate_prompt()

        chunk_batches=batch(data_chunks,batch_size=data_chunks_per_prompt)
        for chunk_batch in tqdm(chunk_batches,total=len(chunk_batches)):
            data_chunk=self.join_data_chunks(data_chunks=chunk_batch)

            with ThreadPoolExecutor() as executor:
                futures = [
                    executor.submit(
                        self.generate_instruction_answer_pair,
                        data_type,
                        data_chunk,
                        model_prompt,
                        model_gpt,
                    ),
                    executor.submit(
                        self.generate_instruction_answer_pair,
                        data_type,
                        data_chunk,
                        model_prompt,
                        model_gemini,
                    ),
                    executor.submit(
                        self.generate_instruction_answer_pair,
                        data_type,
                        data_chunk,
                        model_prompt,
                        model_mistral,
                    ),
                    executor.submit(
                        self.generate_instruction_answer_pair,
                        data_type,
                        data_chunk,
                        model_prompt,
                        model_anthropic,
                    ),
                    executor.submit(
                        self.generate_instruction_answer_pair,
                        data_type,
                        data_chunk,
                        model_prompt,
                        model_cohere,
                    ),
                    executor.submit(
                        self.generate_instruction_answer_pair,
                        data_type,
                        data_chunk,
                        model_prompt,
                        model_groq,
                    ),
                    executor.submit(
                        self.generate_instruction_answer_pair,
                        data_type,
                        data_chunk,
                        model_prompt,
                        model_perplexity,
                    ),
                    executor.submit(
                        self.generate_instruction_answer_pair,
                        data_type,
                        data_chunk,
                        model_prompt,
                        model_deepseek,
                    )
                ]

                for future in as_completed(futures):
                    instruct,ans=future.result()
                    instructions.extend(instruct)
                    answers.extend(ans)


        return instructions,answers




    @abstractmethod
    def generate(self,chunked_documents:list[ChunkedDocumentT]) -> tuple[list,list]:
        pass




