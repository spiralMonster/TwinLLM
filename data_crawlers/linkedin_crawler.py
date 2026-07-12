import time
from loguru import logger

from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By,ByType


from data_crawlers.base_crawler import BaseCrawler
from data_crawlers.base_selenium_crawler import BaseSeleniumCrawler

from document_categories.nosql_db_document_categories.post_document import PostDocument

from utils.exceptions.login_exception import LoginException
from settings import Settings



class LinkedinCrawler(BaseCrawler,BaseSeleniumCrawler):
    document_model=PostDocument


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
        logger.info("Logging into Linkedin..")

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


    def extract(self,link:str,**kwargs) -> None:
        logger.info(f"Scrapping LinkedIn link: {link}")

        self.driver.get(link)
        time.sleep(2)

        driver_current_url=self.driver.current_url
        if "authwall" in driver_current_url:
            self.login()
            time.sleep(3)
            self.driver.get(link)

        self.scroll_page()
        time.sleep(2)

        docs=[]
        dates=[]

        doc_elements=self.driver.find_elements(By.CSS_SELECTOR,'span[dir="ltr"]')
        date_elements=self.driver.find_elements(By.CSS_SELECTOR,".update-components-actor__sub-description")

        user_name=doc_elements[0].text.strip()

        ind=0
        date_ind=0
        num_docs=len(doc_elements)

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

        self.driver.close()

        user=kwargs["user"]
        for doc,date in zip(docs,dates):
            old_document_model=self.document_model.find(
                content=doc,
                published_date=date
            )

            if old_document_model is not None:
                logger.info("The LinkedIn Post already exists")
                continue


            instance=self.document_model(
                content=doc,
                platform="LinkedIn",
                author_id=user.id,
                author_full_name=user.full_name,
                published_date=date,
                link=link
            )

            instance.save()


        logger.info(f"Successfully scrapped and saved the LinkedIn posts for user: {user.full_name}")



