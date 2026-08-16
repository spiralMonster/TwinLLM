from model_inference.base.inference import Inference
from settings import Settings


class InferenceExecutor:
    def __init__(
            self,
            llm:Inference,
            prompt:str
    ) -> None:

        self.llm=llm
        self.prompt=prompt


    def execute(self) -> str:
        inputs=self.prompt
        parameters={
            "max_new_tokens":Settings.MAX_NEW_TOKENS_INFERENCE,
            "repetition_penalty":1.1,
            "temperature":Settings.TEMPERATURE_INFERENCE
        }

        self.llm.set_payload(
            inputs=inputs,
            parameters=parameters
        )

        answer=self.llm.inference()[0]["generated_text"]

        return answer