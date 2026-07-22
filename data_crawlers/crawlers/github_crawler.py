import shutil
import os
import subprocess
import statistics
from loguru import logger
from tempfile import mkdtemp

from data_crawlers.crawlers.base.base_crawler import BaseCrawler
from document_categories.nosql_db_document_categories.repository_document import RepositoryDocument

from utils.extension_to_programming_language import ExtensionToProgrammingLanguage
from utils.exceptions.crawler_exceptions.repository_crawling_exception import RepositoryCrawlingException



class GitHubCrawler(BaseCrawler):
    document_model=RepositoryDocument

    def __init__(
            self,
            ignore=(".git",".gitattributes",".env",".toml",".lock",".png",".jpeg",".jpg",".txt",".json",".csv",".venv",".proto",".tfrecords",".ipynb")
    ) -> None:
        self._ignore=ignore


    def extract(self,link:str,**kwargs) -> tuple[str,dict]:
        old_document_model=self.document_model.find(link=link)

        if old_document_model is not None:
            logger.info("Repository Document already exists in database.")

            metadata={
                "num_successful_crawls":0,
                "mean_content_length":0,
                "median_content_length":0,
                "min_content_length":0,
                "max_content_length":0
            }

            return "github",metadata

        user=kwargs["user"]
        logger.info(f"Scrapping the Github repository: {link} of user: {user.full_name}")

        repo_name=link.rstrip("/").split("/")[-1]

        current_dir=os.getcwd()
        local_temp=mkdtemp()

        try:
            os.chdir(local_temp)
            subprocess.run(["git","clone",link])

            repo_path=os.path.join(local_temp,os.listdir(local_temp)[0])
            tree={}
            programming_languages_used=[]
            file_count=0
            num_successful_crawls=0
            len_crawls=[]

            for root,_,files in os.walk(repo_path):
                directory=root.replace(repo_path,"").lstrip("/")

                if directory.startswith(self._ignore):
                    continue


                for file in files:
                    if file.endswith(self._ignore):
                        continue

                    ind=file.find(".")
                    if ind!=-1:
                        file_extension=file[ind+1:]
                        programming_lang=ExtensionToProgrammingLanguage(extension=file_extension)
                        if programming_lang:
                            if programming_lang not in programming_languages_used:
                                programming_languages_used.append(programming_lang)


                    file_count+=1
                    file_path=os.path.join(directory,file)
                    with open(os.path.join(root,file),"r",errors="ignore") as f:
                        content=f.read()

                    if content:
                        tree[file_path]=content
                        num_successful_crawls+=1

                        len_file=len(tree[file_path].split(" "))
                        len_crawls.append(len_file)


            programming_languages_used=", ".join(programming_languages_used)

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
            os.chdir(current_dir)


        logger.info(f"Finished scrapping the repository {repo_name} of user {user.full_name}")

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
            logger.info("No file extracted from github.")
            metadata={
                "num_successful_crawls":0,
                "mean_content_length":0,
                "median_content_length":0,
                "min_content_length":0,
                "max_content_length":0
            }

        return "github",metadata


