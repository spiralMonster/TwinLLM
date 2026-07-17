import time
import statistics
from loguru import logger
from selenium.webdriver.chrome.options import Options

from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException,StaleElementReferenceException

from data_crawlers.crawlers.base_selenium_crawler import BaseSeleniumCrawler

from document_categories.nosql_db_document_categories.tweet_document import TweetDocument

from utils.exceptions.x_scrapping_exception import XScrappingException
from utils.exceptions.mongo_database_exception import MongoDBException


class XCrawler(BaseSeleniumCrawler):
    document_model=TweetDocument

    def set_extra_driver_options(self,options:Options) -> None:
        options.add_argument("--user-data-dir=.twitter_profile")



    def extract_tweets(self,link:str,page_scroll_limit:int=3) ->list[tuple[str,str]]:
        try:
            self.driver.get(link)
            time.sleep(3)

            driver_current_url=self.driver.current_url
            if "highlights" in driver_current_url:
                tweet_element_expr = 'div[data-testid="tweetText"]'
                date_element_expr = "time"
                author_element_expr = 'div[data-testid="User-Name"]'

            else:
                tweet_element_expr = 'div[class="font-chirp max-w-full whitespace-pre-wrap break-words text-text text-body font-normal"]'
                date_element_expr = 'a[data-state="closed"]'
                author_element_expr = 'div[data-slot="hover-card-trigger"]'


            scroll_ind=0
            tweets=[]
            dates=[]
            author_names=[]

            logger.info("Expanding Show More buttons.")
            while scroll_ind<page_scroll_limit:
                buttons=self.driver.find_elements(
                    By.CSS_SELECTOR,
                    'button[data-testid="tweet-text-show-more-link"]'
                )

                for button in buttons:
                    try:
                        self.driver.execute_script(
                            "arguments[0].scrollIntoView({block:'center'});",
                            button
                        )
                        time.sleep(0.3)

                        self.driver.execute_script(
                            "arguments[0].click();",
                            button
                        )
                        time.sleep(0.3)

                        logger.info("Button clicked.")

                    except NoSuchElementException as e:
                        logger.exception("No more 'Show More' buttons.")
                        logger.exception(f"Exception: {e}")

                    except StaleElementReferenceException as e:
                        logger.exception(f"Exception: {e}")


                logger.info("Scrapping the tweets.")
                tweet_elements=self.driver.find_elements(
                    By.CSS_SELECTOR,
                    tweet_element_expr
                )
                for elem in tweet_elements:
                    tweet=elem.text.strip()
                    if tweet:
                        tweets.append(tweet)


                logger.info("Scrapping the tweet dates.")
                date_elements=self.driver.find_elements(
                    By.CSS_SELECTOR,
                    date_element_expr
                )
                for elem in date_elements:
                    date=elem.text.strip()
                    if date:
                        dates.append(date)


                logger.info("Scrapping the tweet authors.")
                author_names_elements=self.driver.find_elements(
                    By.CSS_SELECTOR,
                    author_element_expr
                )
                for elem in author_names_elements:
                    author=elem.text.split("\n")[0].strip()
                    if author:
                        author_names.append(author)

                self.scroll_page(scroll_limit=1)
                scroll_ind+=1


            author_name=author_names[0]
            final_tweets=[]
            final_dates=[]

            for date,author,tweet in zip(dates,author_names,tweets):
                if author==author_name:
                    final_dates.append(date)
                    final_tweets.append(tweet)


            result=list(zip(final_dates,final_tweets))

            return result

        except Exception as e:
            logger.exception(f"Failed to Scrap the tweets from link: {link}")
            logger.exception(f"Exception: {e}")

            raise XScrappingException("Failed Scrapping X!!!")




    def extract(self,link:str,**kwargs) -> dict:
        user=kwargs["user"]
        logger.info(f"Scrapping the X tweets of user: {user.full_name}")

        username=link.split("/")[-2]

        extracted_tweets=self.extract_tweets(link=link)

        try:
            num_successful_crawls=0
            len_crawls=[]

            for (date,tweet) in extracted_tweets:
                old_document_model=self.document_model.find(
                    content=tweet,
                    published_date=date,
                    username=username
                )

                if old_document_model is not None:
                    logger.info("Tweet already exists in database.")
                    continue

                instance=self.document_model(
                    content=tweet,
                    platform="X",
                    author_id=user.id,
                    author_full_name=user.full_name,
                    username=username,
                    link=link,
                    published_date=date
                )

                instance.save()

                num_successful_crawls+=1

                len_tweet=len(tweet.split(" "))
                len_crawls.append(len_tweet)


        except Exception as e:
            logger.exception(f"Exception: {e}")
            raise MongoDBException("Failed saving the instance in MongoDB!!!!")

        finally:
            self.driver.quit()


        logger.info(f"Successfully scrapped and saved the X tweets in the database of user: {user.full_name}")


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

        return metadata
