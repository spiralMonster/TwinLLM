from loguru import logger

from document_categories.vectordb_document_categories.chunked_documents.post_chunked_document import PostChunkedDocument
from document_categories.instruction_answer_document_categories.post_instruction_answer_document import PostInstructionAnswerDocument
from dataset_generator.instruction_dataset_generator.base.instruction_generator import InstructionGenerator

from utils.exceptions.model_exceptions.instruction_dataset_generator_exception import InstructionDatasetGeneratorException


class InstructionGeneratorFromPosts(InstructionGenerator):
    def create_data_chunks(self, chunks: list[PostChunkedDocument]) -> list[str]:
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
    
    
    def generate(self,chunked_documents:list[PostChunkedDocument]) -> list[PostInstructionAnswerDocument]:
        data_type="post"
        data_chunks=self.create_data_chunks(chunks=chunked_documents)

        temperature=self.MODEL_TEMPERATURE
        max_retries=self.MODEL_MAX_RETRIES
        
        instructions,answers=self.generate_instruction_answer_dataset(
            data_type=data_type,
            data_chunks=data_chunks,
            model_temperature=temperature,
            max_retries=max_retries
        )
        
        len_dataset=len(instructions)
        if len_dataset:
            instruct_ans_docs=[]
            for inst,ans in zip(instructions,answers):
                doc=PostInstructionAnswerDocument(
                    instruction=inst,
                    answer=ans
                )
                instruct_ans_docs.append(doc)


            logger.info(f"{len(instruct_ans_docs)} Instruction-Answer pairs generated from the Post Chunks.")
            return instruct_ans_docs

        
        else:
            logger.info("Failed to generate Instruction-Answer pairs for Post Chunks.")
            raise InstructionDatasetGeneratorException("Failed to generate Instruction-Answer Dataset.")
    