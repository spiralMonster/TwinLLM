import time
from loguru import logger

from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

from data_crawlers.base_selenium_crawler import BaseSeleniumCrawler

from document_categories.nosql_db_document_categories.article_document import ArticleDocument

from utils.exceptions.substack_scrapping_exception import SubstackScrappingException


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


        logger.info(f"Number of Article links extracted successfully: {len(article_links)}")

        return article_links


    def extract(self,link:str,**kwargs) -> None:
        user=kwargs["user"]

        logger.info(f"Scrapping the articles of user: {user.full_name}")
        article_links=self.extract_article_links(
            link=link,
            user=user.full_name
        )

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

                username_element=self.driver.find_element(
                    By.CSS_SELECTOR,
                    'a[href^="https://substack.com/@"]'
                )
                username=username_element.get_attribute("href").split("/")[-1].strip()


                title_element=self.driver.find_elements(
                    By.CSS_SELECTOR,
                    'a[href*="/p/"]'
                )[-1]
                title=title_element.text.strip()

                try:
                    description_element=title_element.find_element(
                        By.XPATH,
                        "./following-sibling::div"
                    )
                    description=description_element.text.strip()

                except Exception as e:
                    logger.exception("No description exists.")
                    description=None


                date_element=username_element.find_element(
                    By.XPATH,
                    "./ancestor::div[2]/div[2]"
                )
                date=date_element.text.strip()


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


            except Exception as e:
                logger.info(f"Exception encountered: {e}")
                logger.info(f"While scrapping substack article: {article_url}")

                raise SubstackScrappingException("Exception encountered.")


        logger.info(f"Successfully scrapped and saved substack articles of user: {user.full_name}")

        self.driver.close()







