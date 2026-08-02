from loguru import logger

from document_categories.vectordb_document_categories.chunked_documents.tweet_chunked_document import TweetChunkedDocument
from document_categories.instruction_answer_document_categories.tweet_instruction_answer_document import TweetInstructionAnswerDocument
from dataset_generator.instruction_dataset_generator.base.instruction_generator import InstructionGenerator

from settings import Settings
from utils.exceptions.model_exceptions.instruction_dataset_generator_exception import InstructionDatasetGeneratorException


class InstructionGeneratorFromTweets(InstructionGenerator):
    def create_data_chunks(self, chunks: list[TweetChunkedDocument]) -> list[str]:
        data_chunks = []

        for chunk in chunks:
            data = f"""
               Metadata:
                - Platform: {chunk.platform}
                - Author: {chunk.author_full_name}
                - Published Date: {chunk.published_date}

               Content:
               {chunk.content}
               """

            data_chunks.append(data)

        return data_chunks
    
    
    def generate(self,chunked_documents:list[TweetChunkedDocument]) -> list[TweetInstructionAnswerDocument]:
        data_type="tweet"
        data_chunks=self.create_data_chunks(chunks=chunked_documents)

        temperature=self.MODEL_TEMPERATURE
        max_retries=self.MODEL_MAX_RETRIES

        models = [
            self.initialize_mistral_model(
                api_key=Settings.MISTRAL_API_KEY4,
                temperature=temperature,
                max_retries=max_retries,
            ),
            self.initialize_cohere_model(
                api_key=Settings.COHERE_API_KEY4,
                temperature=temperature,
                max_retries=max_retries,
            ),
            self.initialize_groq_model(
                api_key=Settings.GROQ_API_KEY4,
                temperature=temperature,
                max_retries=max_retries,
            ),
            self.initialize_qwen_model(
                api_key=Settings.QWEN_API_KEY4,
                temperature=temperature,
                max_retries=max_retries,
            ),
        ]

        
        instructions,answers=self.generate_instruction_answer_dataset(
            models=models,
            data_type=data_type,
            data_chunks=data_chunks
        )
        
        len_dataset=len(instructions)
        if len_dataset:
            instruct_ans_docs=[]
            for inst,ans in zip(instructions,answers):
                doc=TweetInstructionAnswerDocument(
                    instruction=inst,
                    answer=ans
                )
                instruct_ans_docs.append(doc)

            return instruct_ans_docs
        
        else:
            logger.info("Failed to generate Instruction-Answer pairs for Tweet Chunks.")
            raise InstructionDatasetGeneratorException("Failed to generate Instruction-Answer Dataset.")