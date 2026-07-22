import time
import statistics
from loguru import logger

from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By,ByType

from data_crawlers.crawlers.base.base_selenium_crawler import BaseSeleniumCrawler

from document_categories.nosql_db_document_categories.post_document import PostDocument

from settings import Settings

from utils.convert_date_codes_to_date import ConvertCodeToDate

from utils.exceptions.general_exceptions.login_exception import LoginException
from utils.exceptions.crawler_exceptions.linkedin_scrapping_exception import LinkedInScrappingException



class LinkedinCrawler(BaseSeleniumCrawler):
    document_model=PostDocument


    def set_extra_driver_options(self,options:Options) -> None:
        options.add_argument("--user-data-dir=.linkedin_profile")



    def get_visible_element(
            self,
            driver: WebDriver,
            by: ByType,
            value: str,
            text: str|None = None,
            timeout: int = 20
    ) -> WebElement:

        wait=WebDriverWait(driver,timeout)

        def _find():
            elements=driver.find_elements(by,value)

            for elem in elements:
                if not elem.is_displayed():
                    continue

                if not elem.is_enabled():
                    continue

                if text is not None and elem.text.strip()!=text:
                    continue

                return elem

            return False


        element_found=_find()
        if not element_found:
            logger.error("Unable to login try again later!!!")
            raise LoginException("Failed to login")

        final_element=wait.until(element_found)
        return final_element



    def login(self) -> None:
        logger.info("Logging into LinkedIn..")

        self.driver.get("https://www.linkedin.com/login")
        time.sleep(3)

        email=self.get_visible_element(
            driver=self.driver,
            by=By.CSS_SELECTOR,
            value="input[type='email']"
        )

        password=self.get_visible_element(
            driver=self.driver,
            by=By.CSS_SELECTOR,
            value="input['password']"
        )

        linkedin_username=Settings.LINKEDIN_USERNAME
        linkedin_password=Settings.LINKEDIN_PASSWORD

        email.send_keys(linkedin_username)
        password.send_keys(linkedin_password)

        login_button=self.get_visible_element(
            driver=self.driver,
            by=By.TAG_NAME,
            value="button",
            text="Sign in"
        )
        login_button.click()

        logger.info("Successfully logged into LinkedIN.")


    def extract(self,link:str,**kwargs) -> tuple[str,dict]:
        User=kwargs["user"]

        try:
            logger.info(f"Scrapping LinkedIn link: {link} of user: {User.full_name}")

            self.driver.get(link)
            time.sleep(2)

            driver_current_url=self.driver.current_url
            if "authwall" in driver_current_url:
                self.login()
                time.sleep(3)
                self.driver.get(link)

            self.scroll_page()
            time.sleep(2)

            doc_elements=self.driver.find_elements(By.CSS_SELECTOR,'span[dir="ltr"]')
            date_elements=self.driver.find_elements(By.CSS_SELECTOR,".update-components-actor__sub-description")

            docs=[]
            dates=[]

            ind=0
            date_ind=0
            num_docs=len(doc_elements)
            num_dates=len(date_elements)

            if num_dates==num_docs//2:
                user_name = doc_elements[0].text.strip()

                while ind<num_docs:
                    doc_ind=ind+1

                    user=doc_elements[ind].text.strip()
                    doc=doc_elements[doc_ind].text.strip()
                    date=date_elements[date_ind].text.strip().split(" ")[0]

                    if user==user_name:
                        docs.append(doc)
                        dates.append(date)

                    ind+=2
                    date_ind+=1


            else:
                for elem in doc_elements:
                    text=elem.text.strip()
                    if text:
                        if len(text.split(" "))>2:
                            docs.append(text)

                for elem in date_elements:
                    date=elem.text.strip().split(" ")[0]
                    dates.append(date)

                dates=dates[-len(docs):]


            num_successful_crawls=0
            len_crawled_content=[]

            for doc,date in zip(docs,dates):
                date=ConvertCodeToDate(date)

                old_document_model=self.document_model.find(
                    content=doc,
                    published_date=date
                )

                if old_document_model is not None:
                    logger.info("The LinkedIn Post already exists.")
                    continue


                instance=self.document_model(
                    content=doc,
                    platform="LinkedIn",
                    author_id=User.id,
                    author_full_name=User.full_name,
                    published_date=date,
                    link=link
                )

                instance.save()

                num_successful_crawls+=1
                len_post=len(doc.split(" "))
                len_crawled_content.append(len_post)


            logger.info(f"Successfully scrapped and saved {num_successful_crawls} LinkedIn posts for user: {User.full_name}")


        except Exception as e:
            logger.info(f"Exception encountered: {e}")
            logger.info(f"While scrapping LinkedIn link: {link} of user: {User.full_name}")

            raise LinkedInScrappingException("Exception encountered!!!")


        finally:
            self.driver.quit()



        if num_successful_crawls:
            mean_content_length=int(statistics.mean(len_crawled_content))
            median_content_length=int(statistics.median(len_crawled_content))
            min_content_length=int(min(len_crawled_content))
            max_content_length=int(max(len_crawled_content))

            metadata={
                "num_successful_crawls":num_successful_crawls,
                "mean_content_length":mean_content_length,
                "median_content_length":median_content_length,
                "min_content_length":min_content_length,
                "max_content_length":max_content_length
            }

        else:
            logger.info("No LinkedIn post extracted.")
            metadata={
                "num_successful_crawls":0,
                "mean_content_length":0,
                "median_content_length":0,
                "min_content_length":0,
                "max_content_length":0
            }


        return "linkedin",metadata





