from loguru import logger
from tqdm import tqdm
from typing import Annotated

from zenml import step,get_step_context

from document_categories.nosql_db_document_categories.user_document import UserDocument
from data_crawlers.crawler_dispatcher import CrawlerDispatcher

from pipelines.data_etl_pipeline.metadata.get_crawl_links_metadata import _get_metadata_



def _crawl_link(dispatcher: CrawlerDispatcher,link:str,user:UserDocument) -> tuple[str,dict]:
    crawler=dispatcher.get_crawler(url=link)

    crawler_domain,crawler_metadata=crawler.extract(
        link=link,
        user=user
    )


    return crawler_domain,crawler_metadata


@step
def crawl_links(user: UserDocument,links:list[str]) -> Annotated[list[str],"crawled_links"]:
    dispatcher=(CrawlerDispatcher.build()
                .register_linkedin()
                .register_github()
                .register_medium()
                .register_substack()
                .register_x()
                .register_threads())

    logger.info(f"Starting to crawl {len(links)} links of user: {user.full_name}")

    metadata={}
    for link in tqdm(links):
        crawler_domain,crawler_metadata=_crawl_link(
            dispatcher=dispatcher,
            link=link,
            user=user

        )

        metadata=_get_metadata_(
            metadata=metadata,
            crawler_metadata=crawler_metadata,
            domain=crawler_domain
        )


    step_context=get_step_context()
    step_context.add_output_metadata(
        output_name="crawled_links",
        metadata=metadata
    )

    logger.info(f"Successfully crawled links of user: {user.full_name}")

    return links