from model_inference.inference_using_aws.llm_inference_sagemaker_endpoint import LLMInferenceSagemakerEndpoint
from model_inference.inference_executor import InferenceExecutor

from settings import Settings


def call_llm_service(prompt:str) -> str:
    llm=LLMInferenceSagemakerEndpoint(
        endpoint_name=Settings.SAGEMAKER_ENDPOINT_NAME,
        inference_component_name=None
    )

    inference_executor=InferenceExecutor(
        llm=llm,
        prompt=prompt

    )

    answer=inference_executor.execute()
    return answer
