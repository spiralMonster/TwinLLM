import os
import time
import statistics
from loguru import logger
from selenium.webdriver.chrome.options import Options

from selenium.webdriver.common.by import By

from data_crawlers.crawlers.base_selenium_crawler import BaseSeleniumCrawler

from document_categories.nosql_db_document_categories.tweet_document import TweetDocument

from settings import Settings

from utils.exceptions.general_exceptions.login_exception import LoginException
from utils.exceptions.crawler_exceptions.thread_scrapping_exception import ThreadScrappingException
from utils.exceptions.mongodb_exceptions.mongo_database_exception import MongoDBException


class ThreadCrawler(BaseSeleniumCrawler):
    document_model=TweetDocument

    def set_extra_driver_options(self,options:Options) -> None:
        options.add_argument("--user-data-dir=.threads_profile")



    def login(self) -> None:
        try:
            logger.info("Logging into Threads.")

            login_url="https://www.threads.com/login"
            self.driver.get(login_url)
            time.sleep(3)

            username_element=self.driver.find_element(
                By.CSS_SELECTOR,
                'input[placeholder="Username, phone or email"]'

            )

            password_element=self.driver.find_element(
                By.CSS_SELECTOR,
                'input[placeholder="Password"]'

            )

            thread_username=Settings.THREADS_USERNAME
            thread_password=Settings.THREADS_PASSWORD

            username_element.send_keys(thread_username)
            password_element.send_keys(thread_password)

            time.sleep(2)

            login_button=self.driver.find_element(
                By.XPATH,
                "//div[@role='button' and .//div[text()='Log in']]"
            )
            login_button.click()

            logger.info("Successfully logged into Threads.")

        except Exception as e:
            logger.exception(f"Exception: {e}")

            raise LoginException("Exception encountered while logging into Threads")


    def extract_threads(self,link:str,scroll_limit:int=2) -> list[tuple[str,str]]:
        try:
            threads=[]
            dates=[]

            self.driver.get(link)
            time.sleep(2)

            logger.info("Scrapping the threads.")

            scroll_ind=0
            while scroll_ind<scroll_limit:
                thread_elements=self.driver.find_elements(
                    By.CSS_SELECTOR,
                    'div[class="xat24cr x1n2onr6 xdj266r"]'
                )
                for elem in thread_elements:
                    thread=" ".join(elem.text.split("\n")).strip()
                    if thread:
                        threads.append(thread)


                date_elements=self.driver.find_elements(
                    By.CSS_SELECTOR,
                    'time[class="x1rg5ohu xnei2rj x2b8uid xuxw1ft"]'
                )
                for elem in date_elements:
                    date=elem.get_attribute("title")
                    if date:
                        dates.append(date)

                self.scroll_page(scroll_limit=1)
                scroll_ind+=1

            logger.info("Threads scrapped successfully...")

            result=list(zip(dates,threads))

            return result


        except Exception as e:
            logger.exception(f"Exception encountered: {e}")
            raise ThreadScrappingException("Exception encountered while scrapping Threads!!!")



    def extract(self,link:str,**kwargs) -> tuple[str,dict]:
        if os.path.isdir(".threads_profile"):
            logger.info("Already logged in Threads.")


        else:
            self.login()

        user=kwargs["user"]
        username=link.split("/")[-1].strip()[1:]

        logger.info(f"Scrapping the threads from link: {link} of user: {user.full_name}")
        extracted_threads=self.extract_threads(
            link=link,
            scroll_limit=2
        )

        try:
            num_successful_crawls=0
            len_crawls=[]

            for (date,thread) in extracted_threads:
                old_document_model=self.document_model.find(
                    content=thread,
                    published_date=date,
                    username=username
                )

                if old_document_model is not None:
                    logger.info("Thread already exists in database.")
                    continue


                instance=self.document_model(
                    content=thread,
                    platform="Threads",
                    author_id=user.id,
                    author_full_name=user.full_name,
                    username=username,
                    link=link,
                    published_date=date
                )

                instance.save()

                num_successful_crawls+=1

                len_thread=len(thread.split(" "))
                len_crawls.append(len_thread)


        except Exception as e:
            logger.exception(f"Exception encountered: {e}")
            raise MongoDBException(f"Exception encountered while saving threads in MongoDB of user: {user.full_name}")


        finally:
            self.driver.quit()


        logger.info(f"Successfully scrapped and saved {num_successful_crawls} threads in database of user: {user.full_name}")


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
            logger.info("No thread extracted.")
            metadata={
                "num_successful_crawls":0,
                "mean_content_length":0,
                "median_content_length":0,
                "min_content_length":0,
                "max_content_length":0
            }

        return "threads",metadata








