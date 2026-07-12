import shutil
import os
import subprocess
from loguru import logger
from tempfile import mkdtemp

from data_crawlers.base_crawler import BaseCrawler
from document_categories.nosql_db_document_categories.repository_document import RepositoryDocument

from utils.extension_to_programming_language import ExtensionToProgrammingLanguage
from utils.exceptions.repository_crawling_exception import RepositoryCrawlingException



class GitHubCrawler(BaseCrawler):
    document_model=RepositoryDocument

    def __init__(
            self,
            ignore=(".git",".env",".toml",".lock",".png",".jpeg",".md",".txt",".json",".csv",".venv",".proto",".tfrecords")
    ) -> None:
        self._ignore=ignore


    def extract(self,link:str,**kwargs) -> None:
        old_document_model=self.document_model.find(link=link)

        if old_document_model is not None:
            logger.info("Repository Document already exists in database.")

            return

        user=kwargs["user"]
        logger.info(f"Scrapping the Github repository: {link} of user: {user.full_name}")

        repo_name=link.rstrip("/").split("/")[-1]
        local_temp=mkdtemp()

        try:
            os.chdir(local_temp)
            subprocess.run(["git","clone",link])

            repo_path=os.path.join(local_temp,os.listdir(local_temp)[0])
            tree={}
            programming_languages_used=[]
            file_count=0

            for root,_,files in os.walk(repo_path):
                dir=root.replace(repo_path,"").lstrip("/")

                if dir.startswith(self._ignore):
                    continue


                for file in files:
                    if file.endswith(self._ignore):
                        continue

                    ind=file.find(".")
                    if ind!=-1:
                        file_extension=file[ind+1:]
                        programming_lang=ExtensionToProgrammingLanguage(extension=file_extension)
                        if not programming_lang:
                            if programming_lang not in programming_languages_used:
                                programming_languages_used.append(programming_lang)


                    file_count+=1
                    file_path=os.path.join(dir,file)
                    with open(os.path.join(root,file),"r",errors="ignore") as f:
                        tree[file_path]=f.read()


            programming_languages_used=" ".join(programming_languages_used)

            instance=self.document_model(
                content=tree,
                platform="GitHub",
                author_id=user.id,
                author_full_name=user.full_name,
                repository_name=repo_name,
                link=link,
                file_count=file_count,
                programming_languages_used=programming_languages_used
            )

            instance.save()

        except Exception as e:
            logger.exception(f"Exception encountered: {e}")
            raise RepositoryCrawlingException(f"Couldn't scrape the repository: {repo_name}")

        finally:
            shutil.rmtree(local_temp)


        logger.info(f"Finished scrapping the repository {repo_name} of user {user.full_name}")


