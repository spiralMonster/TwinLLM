import numpy as np
from numpy.typing import NDArray
from sentence_transformers.cross_encoder import CrossEncoder

from utils.singleton_meta_class import SingletonMeta
from settings import Settings


class CrossEncoderModel(metaclass=SingletonMeta):
    def __init__(
            self,
            model_id:str=Settings.CROSS_ENCODER_MODEL_ID,
            model_device:str=Settings.EMBEDDING_MODEL_DEVICE
    ) -> None:

        self._model_id=model_id
        self._model_device=model_device

        self.model=CrossEncoder(
            model_name_or_path=self._model_id,
            device=self._model_device
        )

        self.model.model.eval()


    @property
    def model_id(self) -> str:
        _id=self._model_id
        return _id


    def __call__(
            self,
            pairs:list[tuple[str,str]],
            to_list:bool=True
    ) -> NDArray[np.float32]|list[float]:

        scores=self.model.predict(pairs)

        if to_list:
            scores=scores.tolist()


        return scores
