from document_categories.vectordb_document_categories.chunked_documents.base.chunked_document import ChunkedDocument
from dataset_generator.instruction_dataset_generator.dispatcher.instruction_generator_handler import InstructionGeneratorHandler

from document_categories.data_category import DataCategory


class InstructionGeneratorDispatcher:
    instruction_generator_handler=InstructionGeneratorHandler()

    @classmethod
    def dispatch(cls,chunked_documents:list[ChunkedDocument]) -> tuple[list,list]:
        chunk=chunked_documents[0]

        category_name=chunk.get_category()
        data_category=DataCategory(category_name)

        handler=cls.instruction_generator_handler.create_handler(data_category=data_category)
        instructions,answers=handler.generate(chunked_documents=chunked_documents)

        return instructions,answers