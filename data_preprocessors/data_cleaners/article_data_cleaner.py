from loguru import logger

from document_categories.nosql_db_document_categories.article_document import ArticleDocument
from document_categories.vectordb_document_categories.cleaned_documents.cleaned_article_document import CleanedArticleDocument

from data_preprocessors.data_cleaners.base.data_cleaner import DataCleaner

from settings import Settings


class ArticleDataCleaner(DataCleaner):
    def clean(self,document_model:ArticleDocument,min_content_length:int) -> CleanedArticleDocument|None:
        content=document_model.content
        title=document_model.title
        description=document_model.description
        username=document_model.username
        link=document_model.link
        date=document_model.published_date

        if title:
            title=title.capitalize()
            cleaned_title=self.remove_or_replace_non_ascii_characters(
                text=title,
                replace_with=None
            )

        else:
            logger.info("No Title exists.")
            cleaned_title="No Title exists."


        if description:
            cleaned_description=self.remove_or_replace_non_ascii_characters(
                text=description,
                replace_with=None
            )

        else:
            logger.info("No description exists")
            cleaned_description="No description exists."


        if link:
            link=link.strip()
            domains=Settings.ARTICLE_DOMAINS
            if self.is_valid_link(link=link,domains=domains):
                pass

            else:
                logger.info("Invalid Link found.")
                link="No link exists."


        else:
            logger.info("No link exists.")
            link="No link exists."


        if date:
            date=date.strip()
            if self.is_valid_date(date=date):
                pass

            else:
                logger.info("Invalid Date found.")
                date="No date exists"

        else:
            logger.info("No date exists.")
            date="No date exists"


        if username:
            username=username.strip()

        else:
            logger.info("No username exists.")
            username="No username exists."


        #Removing extra spaces:
        content=self.remove_extra_spaces(text=content)

        #Replacing urls:
        content=self.remove_or_replace_url(text=content,replace_with="<url>")

        #Removing or replacing Non-ascii characters:
        cleaned_content=self.remove_or_replace_non_ascii_characters(
            text=content,
            replace_with=None
        )


        cleaned_content_length=self.get_content_length(content=cleaned_content)
        if cleaned_content_length<min_content_length:
            logger.info("The length of the content is less than minimum content length.")
            return None


        else:
            cleaned_article=CleanedArticleDocument(
                content=cleaned_content,
                platform=document_model.platform,
                author_id=document_model.author_id,
                author_full_name=document_model.author_full_name,
                username=username,
                title=cleaned_title,
                description=cleaned_description,
                link=link,
                published_date=date
            )

            return cleaned_article


