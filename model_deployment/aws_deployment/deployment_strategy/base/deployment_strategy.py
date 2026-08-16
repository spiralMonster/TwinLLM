import enum
from abc import abstractmethod,ABC
from typing import Optional

class DeploymentStrategy(ABC):
    @abstractmethod
    def deploy(
            self,
            role_arn:str,
            llm_image:str,
            config:dict,
            endpoint_name:str,
            endpoint_config_name:str,
            gpu_instance_type:str,
            resources:Optional[dict],
            endpoint_type:enum.Enum
    ) -> None:
        pass