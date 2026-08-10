from pydantic import BaseModel,Field
from typing import List


class PreferenceTriplet(BaseModel):
    instruction:str=Field(description="The generated instruction.")
    chosen_answer:str=Field(description="The generated chosen answer.")
    rejected_answer:str=Field(description="The generated rejected answer.")



class PreferenceDatasetGeneratorSpecs(BaseModel):
    triplets:List[PreferenceTriplet]=Field(description="""
    The list of generated triplets consisting of instruction,chosen and rejected answer.
    """)