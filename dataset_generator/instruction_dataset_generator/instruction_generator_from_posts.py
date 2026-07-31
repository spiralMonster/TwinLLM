from loguru import logger

from document_categories.vectordb_document_categories.chunked_documents.post_chunked_document import PostChunkedDocument
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
    
    
    def generate(self,chunked_documents:list[PostChunkedDocument]) -> tuple[list,list]:
        data_type="post"
        data_chunks=self.create_data_chunks(chunks=chunked_documents)
        
        instructions,answers=self.generate_instruction_answer_dataset(
            data_type=data_type,
            data_chunks=data_chunks
        )
        
        len_dataset=len(instructions)
        if len_dataset:
            logger.info(f"{len_dataset} Instruction-Answer pairs generated from the Post Chunks.")
            return instructions, answers
        
        else:
            logger.info("Failed to generate Instruction-Answer pairs for Post Chunks.")
            raise InstructionDatasetGeneratorException("Failed to generate Instruction-Answer Dataset.")
    