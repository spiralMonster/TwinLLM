from loguru import logger

from document_categories.nosql_db_document_categories.tweet_document import TweetDocument
from document_categories.vectordb_document_categories.cleaned_documents.cleaned_tweet_document import CleanedTweetDocument

from data_preprocessors.data_cleaners.base.data_cleaner import DataCleaner

from settings import Settings


class TweetDataCleaner(DataCleaner):
    def clean(self,document_model:TweetDocument,minimum_content_length:int) -> CleanedTweetDocument|None:
        content=document_model.content
        username=document_model.username
        link=document_model.link
        date=document_model.published_date

        if username:
            username=username.strip()

        else:
            logger.info("No username exists.")
            username="No username exists"


        if link:
            link=link.strip()
            domains=Settings.TWEET_DOMAINS
            if self.is_valid_link(link=link,domains=domains):
                pass

            else:
                logger.info("Invalid link found.")
                link="No link exists."

        else:
            logger.info("No link exists.")
            link="No link exists."


        if date:
            date=date.strip()
            if self.is_valid_date(date=date):
                pass

            else:
                logger.info("Invalid date found.")
                date="No date exists."

        else:
            logger.info("No date exists.")
            date="No date exists."

        #Removing extra spaces:
        content=self.remove_extra_spaces(text=content)

        #Replacing urls:
        content=self.remove_or_replace_url(text=content,replace_with="<url>")

        #Replacing Non-ascii characters:
        cleaned_content=self.remove_or_replace_non_ascii_characters(
            text=content,
            replace_with="<emoji>"
        )


        content_length=self.get_content_length(content=cleaned_content)
        if content_length<minimum_content_length:
            logger.info("The length of the content is less than minimum content length.")
            return None

        else:
            cleaned_tweet=CleanedTweetDocument(
                content=cleaned_content,
                platform=document_model.platform,
                author_id=document_model.author_id,
                author_full_name=document_model.author_full_name,
                username=username,
                link=link,
                published_date=date
            )

            return cleaned_tweet
