from abc import abstractmethod,ABC
from typing import Any,Dict,Optional


class Inference(ABC):
    def __init__(self):
        self.model=None

    @abstractmethod
    def set_payload(self,inputs:str,parameters:Optional[Dict[str,Any]]):
        pass

    @abstractmethod
    def inference(self):
        pass