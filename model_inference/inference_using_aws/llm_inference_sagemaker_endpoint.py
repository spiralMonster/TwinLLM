import json
from typing import Any,Dict,Optional
from loguru import logger

import boto3
from model_inference.base.inference import Inference

from settings import Settings
from utils.exceptions.model_exceptions.model_inference_exception import ModelInferenceException


class LLMInferenceSagemakerEndpoint(Inference):
    def __init__(
            self,
            endpoint_name:str,
            default_payload:Optional[Dict[str,Any]]=None,
            inference_component_name:Optional[str]=None
    ) -> None:
        super().__init__()

        self.client=boto3.client(
            "sagemaker-runtime",
            region_name=Settings.AWS_REGION,
            aws_access_key_id=Settings.AWS_ACCESS_KEY,
            aws_secret_access_key=Settings.AWS_SECRET_KEY
        )

        self.endpoint_name=endpoint_name
        self.inference_component_name=inference_component_name

        if not default_payload:
            self.payload=self._default_payload()


    @staticmethod
    def _default_payload() -> Dict[str,Any]:
        payload={
            "inputs":"Can you explain me about supervised fine-tuning?",
            "parameters":{
                "max_new_tokens":Settings.MAX_NEW_TOKENS_INFERENCE,
                "top_p":Settings.TOP_P_INFERENCE,
                "temperature":Settings.TEMPERATURE_INFERENCE,
                "return_full_text":False
            }

        }

        return payload


    def set_payload(self,inputs:str,parameters:Optional[Dict[str,Any]]):
        self.payload["inputs"]=inputs

        if parameters:
            self.payload["parameters"].update(parameters)


    def inference(self) ->str:
        try:
            logger.info("Inference Request Sent.")

            invoke_args={
                "EndpointName":self.endpoint_name,
                "ContentType":"application/json",
                "Body":json.dumps(self.payload)
            }

            if self.inference_component_name not in ["None",None]:
                invoke_args["InferenceComponentName"]=self.inference_component_name


            response=self.client.invoke_endpoint(**invoke_args)
            response_body=response["Body"].read().decode("utf8")

            result=json.loads(response_body)
            result=result[0]["generated_text"]

            logger.info("Response generated from the Model Successfully.")
            return result

        except Exception as e:
            logger.info(f"Exception Encountered: {e}")
            raise ModelInferenceException("Failed to generated the inference from the model deployed on AWS SageMaker.")



