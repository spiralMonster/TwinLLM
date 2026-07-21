import time
import statistics
from loguru import logger

from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

from data_crawlers.crawlers.base_selenium_crawler import BaseSeleniumCrawler

from document_categories.nosql_db_document_categories.article_document import ArticleDocument

from utils.exceptions.crawler_exceptions.substack_scrapping_exception import SubstackScrappingException


class SubstackCrawler(BaseSeleniumCrawler):
    document_model=ArticleDocument

    def set_extra_driver_options(self,options:Options) -> None:
        options.add_argument("--user-data-dir=.substack_profile")



    def extract_article_links(self,link:str,user:str) -> list[str]:
        logger.info(f"Extracting Substack Article links of user: {user}")
        article_links=[]

        self.driver.get(link)
        self.scroll_page()
        time.sleep(3)

        link_elements=self.driver.find_elements(
            By.CSS_SELECTOR,
            "a[data-native='true']"
        )

        for elem in link_elements:
            link=elem.get_attribute("href")
            if link:
                article_links.append(link)


        logger.info(f"Number of Substack Article links extracted successfully: {len(article_links)}")

        return article_links


    def extract(self,link:str,**kwargs) -> tuple[str,dict]:
        user=kwargs["user"]

        username=link.split("/")[-2][1:]

        logger.info(f"Scrapping the articles of user: {user.full_name}")
        article_links=self.extract_article_links(
            link=link,
            user=user.full_name
        )

        num_successful_crawls=0
        len_crawls=[]

        for article_url in article_links:
            old_document_model=self.document_model.find(
                link=article_url
            )

            if old_document_model is not None:
                logger.info(f"Article: {article_url} already exists in database.")
                continue

            logger.info(f"Scrapping substack article: {article_url} of user: {user.full_name}")

            try:
                self.driver.get(article_url)
                time.sleep(3)

                try:
                    title_element=self.driver.find_element(
                        By.CSS_SELECTOR,
                        'h1[class="post-title published title-X77sOw"]'
                    )
                    title=title_element.text.strip()

                except Exception as e:
                    logger.info("Failed to extract Title.")
                    title=None

                try:
                    description_element=self.driver.find_element(
                        By.CSS_SELECTOR,
                        'h3.subtitle'
                    )
                    description=description_element.text.strip()

                except Exception as e:
                    logger.info("Failed to extract description.")
                    description=None


                try:
                    date_element=self.driver.find_element(
                        By.CSS_SELECTOR,
                        'div[aria-label="Post UFI"]'
                    )
                    date=date_element.text.split("\n")[1].strip()

                except Exception as e:
                    logger.info("Failed to extract Date.")
                    date=None


                paragraph_elements=self.driver.find_elements(
                    By.CSS_SELECTOR,
                    "p"
                )[1:]

                paragraph=""
                for elem in paragraph_elements:
                    text=elem.text.strip()
                    if text:
                        paragraph+=text
                        paragraph+=" "

                paragraph=paragraph.strip()

                if not paragraph:
                    logger.info("Failed to retrieve the article.")
                    logger.info(f"Skipping the link: {article_url}")
                    continue


                else:
                    instance=self.document_model(
                        content=paragraph,
                        platform="Substack",
                        author_id=user.id,
                        author_full_name=user.full_name,
                        username=username,
                        title=title,
                        description=description,
                        link=article_url,
                        published_date=date

                    )

                    instance.save()

                    logger.info(f"Saved substack article: {article_url} in database.")

                    num_successful_crawls+=1

                    length_article=len(paragraph.split(" "))
                    len_crawls.append(length_article)


            except Exception as e:
                logger.info(f"Exception encountered: {e}")
                logger.info(f"While scrapping substack article: {article_url}")

                raise SubstackScrappingException("Exception encountered.")


        logger.info(f"Successfully scrapped and saved {num_successful_crawls} substack articles of user: {user.full_name}")
        self.driver.quit()

        if num_successful_crawls:
            mean_content_length=int(statistics.mean(len_crawls))
            median_content_length=int(statistics.median(len_crawls))
            min_content_length=int(min(len_crawls))
            max_content_length=int(max(len_crawls))

            metadata={
                "num_successful_crawls":num_successful_crawls,
                "mean_content_length":mean_content_length,
                "median_content_length":median_content_length,
                "min_content_length":min_content_length,
                "max_content_length":max_content_length
            }

        else:
            logger.info("No substack article extracted.")
            metadata={
                "num_successful_crawls":0,
                "mean_content_length":0,
                "median_content_length":0,
                "min_content_length":0,
                "max_content_length":0
            }

        return "substack",metadata







