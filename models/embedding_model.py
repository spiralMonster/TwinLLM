from loguru import logger
from functools import cached_property
from typing import Optional

import numpy as np
from numpy.typing import NDArray

from sentence_transformers.SentenceTransformer import SentenceTransformer
from transformers import AutoTokenizer

from utils.singleton_meta_class import SingletonMeta
from utils.exceptions.model_exceptions.embedding_generation_exception import EmbeddingGenerationException

from settings import Settings


class EmbeddingModel(metaclass=SingletonMeta):
    def __init__(
            self,
            model_id: str = Settings.EMBEDDING_MODEL_ID,
            device: str = Settings.EMBEDDING_MODEL_DEVICE,
            cache_dir: Optional[str] = None
    ) -> None:

        self._model_id=model_id
        self.device=device

        self.model=SentenceTransformer(
            self._model_id,
            device=self.device,
            cache_folder=cache_dir if cache_dir else None,
        )
        self.model.eval()



    @property
    def model_id(self) -> str:
        return self._model_id


    @cached_property
    def embedding_size(self) -> int:
        dummy_embedding=self.model.encode("")
        embedding_size=dummy_embedding.shape[0]

        return embedding_size

    @property
    def max_input_length(self) -> int:
        max_inp_length=self.model.max_seq_length

        return max_inp_length

    @property
    def tokenizer(self) -> AutoTokenizer:
        tokenizer=self.model.tokenizer

        return tokenizer


    def __call__(
            self,
            input_text: str|list[str],
            to_list: bool = True
    ) -> NDArray[np.float32]|list[float]|list[list[float]]:

        try:
            embedding=self.model.encode(input_text)

        except Exception as e:
            logger.error("Error generating embeddings")
            logger.info(f"Error encountered: {e}")

            raise EmbeddingGenerationException("Failed to generate embeddings.")

        if to_list:
            embedding=embedding.tolist()


        return embedding