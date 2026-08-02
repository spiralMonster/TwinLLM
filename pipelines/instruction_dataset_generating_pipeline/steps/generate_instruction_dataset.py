import time
from loguru import logger
from typing import Annotated

from zenml import step,get_step_context
from datasets import Dataset

from document_categories.vectordb_document_categories.chunked_documents.base.chunked_document import ChunkedDocument

from dataset_generator.instruction_dataset_generator.base.instruction_generator import InstructionGenerator
from dataset_generator.instruction_dataset_generator.dispatcher.instruction_generator_dispatcher import InstructionGeneratorDispatcher

from pipelines.instruction_dataset_generating_pipeline.metadata.generate_instruction_dataset_metadata import get_metadata

from document_categories.data_category import DataCategory

from utils.batch_data import batch
from utils.exceptions.model_exceptions.instruction_dataset_generator_exception import InstructionDatasetGeneratorException


@step
def generate_instruction_dataset(
        chunked_documents:Annotated[list[ChunkedDocument],"chunked_documents"]
) -> Annotated[Dataset,"instruction_dataset"]:

    instruction_answer_docs=[]

    grouped_documents=ChunkedDocument.group_by_class(chunked_documents)
    for document_class,documents in grouped_documents.items():
        document_category=document_class.get_category()
        if document_category==DataCategory.REPOSITORIES:
            documents=documents[:100]
        
        logger.info(f"{len(documents)} {document_category} Data Chunks retrieved successfully.")
        logger.info(f"Creating the Instruction-Answer dataset from {document_category} data chunks.")

        num_docs_created=0
        batched_chunks=batch(documents,batch_size=30)
        for chunk_batch in batched_chunks:
            instruct_ans_doc=InstructionGeneratorDispatcher.dispatch(chunked_documents=chunk_batch)
            num_docs_created+=len(instruct_ans_doc)
            if instruct_ans_doc:
                instruction_answer_docs.extend(instruct_ans_doc)

            time.sleep(3)

        logger.info(f"{num_docs_created} Instruction-Answer Pairs created successfully from {document_category} Data Chunks.")




    if instruction_answer_docs:
        instructions=[]
        answers=[]

        for doc in instruction_answer_docs:
            instructions.append(doc.instruction)
            answers.append(doc.answer)


        metadata=dict()
        metadata["model_settings"]={
            "temperature":InstructionGenerator.MODEL_TEMPERATURE,
            "max_retries":InstructionGenerator.MODEL_MAX_RETRIES,
            "llm_used":InstructionGenerator.llm_models_used()
        }

        _metadata=get_metadata(documents=instruction_answer_docs)
        metadata["instruction-answer_datset"]=_metadata

        step_context=get_step_context()
        step_context.add_output_metadata(
            output_name="instruction_dataset",
            metadata=metadata
        )

        final_dataset=Dataset.from_dict(
            {
                "instructions":instructions,
                "outputs":answers
            }
        )

        logger.info(f"Successfully created {len(instruction_answer_docs)} Instruction-Answer pairs from Data Chunks.")
        return final_dataset


    else:
        logger.info("No Instruction-Answer pair document created...")
        raise InstructionDatasetGeneratorException("Failed to generate Instruction-Answer Dataset!!!")