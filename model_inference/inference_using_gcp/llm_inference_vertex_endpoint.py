from loguru import logger
from typing import Any,Dict,Optional

from model_deployment.gcp_deployment.deployment.endpoint_manager import EndpointManager
from model_inference.base.inference import Inference

from settings import Settings
from utils.exceptions.model_exceptions.model_inference_exception import ModelInferenceException


class LLMInferenceVertexEndpoint(Inference):
    def __init__(
            self,
            endpoint_manager:EndpointManager,
            default_payload:Optional[Dict[str,Any]]=None
    ) -> None:
        super().__init__()

        self.endpoint_manager=endpoint_manager

        if not default_payload:
            self.payload=self._default_payload()

        else:
            self.payload=default_payload


    @staticmethod
    def _default_payload() -> Dict[str,Any]:
        payload={
            "prompt":"Can you explain me about supervised fine tuning in detail?",
            "parameters":{
                "max_new_tokens":Settings.MAX_NEW_TOKENS_INFERENCE,
                "temperature":Settings.TEMPERATURE_INFERENCE,
                "top_p":Settings.TOP_P_INFERENCE,
                "do_sample":True
            }
        }

        return payload


    def set_payload(self,inputs:str,parameters:Optional[Dict[str,Any]]) -> None:
        self.payload["prompt"]=inputs

        if parameters:
            self.payload["parameters"].update(parameters)



    def inference(self) -> str:
        try:
            logger.info("Sending Inference Request to Vertex AI Endpoint")

            endpoint=self.endpoint_manager.get_endpoint()

            response=endpoint.predict(
                instances=[
                    self.payload
                ]
            )

            result=response.predictions[0]["prediction"]

            logger.info("Response generated from the Model Successfully.")
            return result

        except Exception as e:
            logger.exception("Failed to generate the response from the Model.")
            raise ModelInferenceException(
                "Failed to generated the response from the Model deployed on Vertex AI."
            ) from e




if __name__=="__main__":
    from model_deployment.gcp_deployment.deployment.endpoint_manager import EndpointManager
    from model_inference.inference_executor import InferenceExecutor

    endpoint_manager=EndpointManager()
    llm=LLMInferenceVertexEndpoint(
        endpoint_manager=endpoint_manager
    )

    alpaca_template="""
    Below is an instruction that describes a task.Write a response that appropriately completes the request.
    
    ### Instruction:
    {}
    
    ### Response:
    """
    query="Can you explain me about supervised fine tuning?"
    prompt=alpaca_template.format(query,"")

    inference_executor=InferenceExecutor(
        llm=llm,
        prompt=prompt
    )

    answer=inference_executor.execute()
    print(f"User: {query}")
    print(f"Twin LLM: {answer}")