from sagemaker.compute_resource_requirements.resource_requirements import ResourceRequirements
from settings import Settings


model_resource_config=ResourceRequirements(
    requests={
        "copies":Settings.NUM_OF_REPLICAS,
        "num_accelerators":Settings.NUM_OF_GPU,
        "num_cpus":Settings.NUM_OF_CPU_CORES,
        "memory":Settings.MIN_MEMORY
    }
)