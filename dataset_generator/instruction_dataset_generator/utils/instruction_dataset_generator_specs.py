from typing import List
from pydantic import BaseModel,Field


class InstructionAnswerPair(BaseModel):
    instruction:str=Field(description="The generated instruction from the data chunk.")
    answer:str=Field(description="The generated answer of the given instruction.")



class InstructionDatasetGeneratorSpecs(BaseModel):
    instruction_answer_pair:List[InstructionAnswerPair]=Field(
        description="The list of generated instruction-answer pair."
    )