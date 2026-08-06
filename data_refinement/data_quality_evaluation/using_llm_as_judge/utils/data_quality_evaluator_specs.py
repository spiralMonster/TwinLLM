from pydantic import BaseModel,Field
from typing import List


class DataQualityMetrics(BaseModel):
    helpfulness:int=Field(description="The helpfulness of the content.")
    correctness:int=Field(description="The correctness of the content.")
    coherence:int=Field(description="The coherence of the content.")
    complexity:int=Field(description="The complexity of the content.")
    relevance:int=Field(description="The relevance of the content.")
    verbosity:int=Field(description="The verbosity of the content.")


class DataQualityEvaluatorSpecs(BaseModel):
    evaluation_results:List[DataQualityMetrics]=Field(description="The list of evaluation metrics of instruction-output pairs.")