import re
from loguru import logger
from urllib.parse import urlparse

from data_crawlers.crawlers.base_crawler import BaseCrawler
from data_crawlers.crawlers.linkedin_crawler import LinkedinCrawler
from data_crawlers.crawlers.github_crawler import GitHubCrawler
from data_crawlers.crawlers.medium_crawler import MediumCrawler
from data_crawlers.crawlers.substack_crawler import SubstackCrawler
from data_crawlers.crawlers.x_crawler import XCrawler
from data_crawlers.crawlers.thread_crawler import ThreadCrawler

from utils.exceptions.no_crawler_found_exception import NoCrawlerFoundException


class CrawlerDispatcher:
    def __init__(self) -> None:
        self._crawlers={}

    @classmethod
    def build(cls) -> "CrawlerDispatcher":
        dispatcher=cls()

        return dispatcher



    def register(self,domain:str,crawler:type[BaseCrawler]) -> None:
        parsed_domain=urlparse(domain)
        domain=parsed_domain.netloc

        crawler_type=r"https://(www\.)?{}.*".format(re.escape(domain))

        self._crawlers[crawler_type]=crawler


    def register_linkedin(self) -> "CrawlerDispatcher":
        self.register("https://linkedin.com",LinkedinCrawler)

        return self


    def register_github(self) -> "CrawlerDispatcher":
        self.register("https://github.com",GitHubCrawler)

        return self


    def register_medium(self) -> "CrawlerDispatcher":
        self.register("https://medium.com",MediumCrawler)

        return self


    def register_substack(self) -> "CrawlerDispatcher":
        self.register("https://substack.com",SubstackCrawler)

        return self


    def register_x(self) -> "CrawlerDispatcher":
        self.register("https://x.com",XCrawler)

        return self


    def register_threads(self) -> "CrawlerDispatcher":
        self.register("https://threads.com",ThreadCrawler)

        return self


    def get_crawler(self,url:str) -> BaseCrawler:
        for crawler_type,crawler in self._crawlers.items():
            if re.match(crawler_type,url):
                return crawler()

        else:
            logger.warning(f"No crawler found for url: {url}")

            raise NoCrawlerFoundException("No crawler found!!!")









