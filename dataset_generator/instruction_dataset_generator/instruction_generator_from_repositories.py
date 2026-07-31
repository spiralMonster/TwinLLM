from loguru import logger

from document_categories.vectordb_document_categories.chunked_documents.repository_chunked_document import RepositoryChunkedDocument
from dataset_generator.instruction_dataset_generator.base.instruction_generator import InstructionGenerator

from utils.exceptions.model_exceptions.instruction_dataset_generator_exception import InstructionDatasetGeneratorException


class InstructionGeneratorFromRepositories(InstructionGenerator):
    def create_data_chunks(self, chunks: list[RepositoryChunkedDocument]) -> list[str]:
        data_chunks = []

        for chunk in chunks:
            file_name=chunk.file_name
            if file_name:
                if not file_name.endswith("md"):
                    data = f"""
                    Metadata:
                     - Platform: {chunk.platform}
                     - Author: {chunk.author_full_name}
                     - Repository Name: {chunk.repository_name}
                     - File Name: {chunk.file_name}
                     - Programming Language Used: {chunk.programming_language_used}
        
                    Content:
                    {chunk.content}
                    """
        
                    data_chunks.append(data)

        return data_chunks
    
    
    def generate(self,chunked_documents:list[RepositoryChunkedDocument]) -> tuple[list,list]:
        data_type="github code"
        data_chunks=self.create_data_chunks(chunks=chunked_documents)
        
        instructions,answers=self.generate_instruction_answer_dataset(
            data_type=data_type,
            data_chunks=data_chunks
        )
        
        len_dataset=len(instructions)
        if len_dataset:
            logger.info(f"{len_dataset} Instruction-Answer pairs generated from the Repository Chunks.")
            return instructions, answers
        
        else:
            logger.info("Failed to generate Instruction-Answer pairs for Repository Chunks.")
            raise InstructionDatasetGeneratorException("Failed to generate Instruction-Answer Dataset.")