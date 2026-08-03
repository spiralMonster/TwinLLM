from loguru import logger

import torch
from transformers import AutoTokenizer,AutoModelForSequenceClassification

from settings import Settings

from utils.singleton_meta_class import SingletonMeta


class ToxicityDetectionModel(metaclass=SingletonMeta):
    def __init__(
            self,
            model_id:str=Settings.TOXICITY_DETECTION_MODEL_ID,
            model_device:str=Settings.TOXICITY_DETECTION_MODEL_DEVICE
    ) -> None:

        self._model_id=model_id
        self._model_device=model_device

        self.model_tokenizer=AutoTokenizer.from_pretrained(
            self._model_id
        )

        self.model=AutoModelForSequenceClassification.from_pretrained(
            self._model_id
        )

        self.id2label=self.model.config.id2label



    @property
    def model_id(self) -> str:
        m_id=self._model_id
        return m_id


    def score_to_label(self,model_scores:torch.Tensor) -> list[dict[str,float]]:
        results=[]
        for scores in model_scores:
            result=dict()
            for ind,score in enumerate(scores):
                label=self.id2label[ind]
                result[label]=float(score)

            results.append(result)

        return results


    def __call__(self,texts:list[str]) -> list[dict[str,float]]:
        model_inputs=self.model_tokenizer(
            texts,
            return_tensors="pt",
            truncation=True,
            padding=True
        )

        with torch.no_grad():
            model_outputs=self.model(
                **model_inputs
            )

        model_scores=torch.sigmoid(model_outputs.logits)

        result=self.score_to_label(model_scores=model_scores)
        return result



