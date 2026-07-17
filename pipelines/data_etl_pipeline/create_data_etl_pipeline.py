from zenml import pipeline

from pipelines.data_etl_pipeline.steps.get_or_create_user import get_or_create_user
from pipelines.data_etl_pipeline.steps.crawl_links import crawl_links



@pipeline
def run_data_etl_pipeline(user_full_name:str,links:list[str]) -> str:
    user=get_or_create_user(user_full_name=user_full_name)
    last_step=crawl_links(user=user,links=links)

    return last_step.invocation_id