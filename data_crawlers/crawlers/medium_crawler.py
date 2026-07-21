import time
from loguru import logger

from selenium.webdriver.common.by import By

from data_crawlers.crawlers.base_selenium_crawler import BaseSeleniumCrawler

from document_categories.nosql_db_document_categories.article_document import ArticleDocument

from utils.exceptions.crawler_exceptions.medium_scrapping_exception import MediumArticleScrappingException


class MediumCrawler(BaseSeleniumCrawler):
    document_model=ArticleDocument

    def extract(self,link:str,**kwargs) -> tuple[str,dict]:
        old_model=self.document_model.find(
            link=link
        )

        if old_model is not None:
            logger.info("Article already exists in database.")

            metadata={
                "num_successful_crawls":0,
                "mean_content_length":0,
                "median_content_length":0,
                "min_content_length":0,
                "max_content_length":0
            }

            return "medium",metadata

        user=kwargs["user"]

        try:
            logger.info(f"Scraping the Medium article: {link}")

            self.driver.get(link)
            time.sleep(3)

            try:
                title_element=self.driver.find_element(
                    By.CSS_SELECTOR,
                    "h1.pw-post-title"
                )
                title=title_element.text.strip()

            except Exception as e:
                logger.info("Failed to extract the title of the article.")
                title=None

            try:
                description_element=self.driver.find_elemenet(
                    By.CSS_SELECTOR,
                    "h2.pw-subtitle-paragraph"
                )
                description=description_element.text.strip()

            except Exception as e:
                logger.info("Failed to extract the description of the article.")
                description=None


            try:
                date_element=self.driver.find_element(
                    By.CSS_SELECTOR,
                    'span[data-testid="storyPublishDate"]'
                )
                published_date=date_element.text.strip()


            except Exception as e:
                logger.info("Failed to extract the date of the article")
                published_date=None


            paragraph_elements=self.driver.find_elements(
                By.CSS_SELECTOR,
                "p.pw-post-body-paragraph"
            )

            paragraph=""
            for elem in paragraph_elements:
                text=elem.text.strip()
                if text:
                    paragraph+=text
                    paragraph+=" "



            if paragraph:
                instance=self.document_model(
                    content=paragraph,
                    platform="Medium",
                    author_id=user.id,
                    author_full_name=user.full_name,
                    title=title,
                    description=description,
                    link=link,
                    published_date=published_date
                )

                instance.save()

                num_successful_crawls=1
                article_length=len(paragraph.split(" "))

                logger.info(f"Successfully scrapped and saved the medium article: {link} of user: {user.full_name}")

            else:
                num_successful_crawls=0
                article_length=0

                logger.info(f"Failed to scrape the medium article: {link} of user: {user.full_name}")



        except Exception as e:
            logger.info(f"Exception encountered: {e}")
            logger.info(f"While scrapping medium article: {link}")

            raise MediumArticleScrappingException("Exception encountered!!!")


        finally:
            self.driver.quit()


        metadata={
            "num_successful_crawls":num_successful_crawls,
            "mean_content_length":article_length,
            "median_content_length":article_length,
            "min_content_length":article_length,
            "max_content_length":article_length,
        }

        return "medium",metadata


