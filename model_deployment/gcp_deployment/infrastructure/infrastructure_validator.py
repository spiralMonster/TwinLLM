from loguru import logger
from google.cloud import compute_v1

from settings import Settings



class InfrastructureValidator:
    def __init__(self) -> None:
        self.region_client=compute_v1.RegionsClient()
        self.accelerator_client=compute_v1.AcceleratorTypesClient()


    def check_quotas(self) -> bool:
        logger.info(f"Checking if GPU is available in region: {Settings.GCP_REGION}")

        region=self.region_client.get(
            project=Settings.GCP_PROJECT_ID,
            region=Settings.GCP_REGION
        )

        gpu_quotas=[]
        for quota in region.quotas:
            if "GPU" in quota.metric.upper() or "ACCELERATOR" in quota.metric.upper():
                gpu_quotas.append(quota)


        if not gpu_quotas:
            logger.info(f"No GPUs available for region: {Settings.GCP_REGION}")
            return False

        has_available_quota=False
        for quota in gpu_quotas:
            available=quota.limit-quota.usage

            if available>0:
                has_available_quota=True


        if not has_available_quota:
            logger.info("The GPU quota has reached the limit.")
            return False

        logger.info(f"The GPU is available to use in the region: {Settings.GCP_REGION}")
        return True


    def check_gpu(self) -> bool:
        logger.info(f"Checking the availability of {Settings.GCP_ACCELERATOR_TYPE_FOR_INFRASTRUCTURE_VALIDATION}")
        client=self.accelerator_client

        request=compute_v1.AggregatedListAcceleratorTypesRequest(
            project=Settings.GCP_PROJECT_ID,
            filter=f"name={Settings.GCP_ACCELERATOR_TYPE_FOR_INFRASTRUCTURE_VALIDATION}"
        )
        response=client.aggregated_list(request=request)

        is_available=False
        available_zones=[]
        for _,scoped_list in response:
            if scoped_list.accelerator_types is None:
                continue

            for accelerator in scoped_list.accelerator_types:
                zone=accelerator.zone.split("/")[-1]
                available_zones.append(zone)
                

        if available_zones:
            is_available=True
            logger.info(f"{Settings.GCP_ACCELERATOR_TYPE_FOR_INFRASTRUCTURE_VALIDATION} is available.")
            return is_available

        else:
            logger.info(f"{Settings.GCP_ACCELERATOR_TYPE_FOR_INFRASTRUCTURE_VALIDATION} is not available.")
            return is_available





if __name__=="__main__":
    infrastructure_validator=InfrastructureValidator()
    infrastructure_validator.check_quotas()
    infrastructure_validator.check_gpu()
