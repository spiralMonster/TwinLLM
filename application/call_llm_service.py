from model_inference.inference_executor import InferenceExecutor

from model_inference.inference_using_aws.llm_inference_sagemaker_endpoint import LLMInferenceSagemakerEndpoint
from model_inference.inference_using_gcp.llm_inference_vertex_endpoint import LLMInferenceVertexEndpoint

from settings import Settings


def call_llm_service_using_aws(prompt:str) -> str:
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


def call_llm_service_using_gcp(prompt:str) -> str:
    from model_deployment.gcp_deployment.deployment.endpoint_manager import EndpointManager

    endpoint_manager=EndpointManager()
    llm=LLMInferenceVertexEndpoint(
        endpoint_manager=endpoint_manager
    )

    inference_executor=InferenceExecutor(
        llm=llm,
        prompt=prompt
    )

    answer=inference_executor.execute()
    return answer
