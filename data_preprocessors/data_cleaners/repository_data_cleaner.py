import re
from loguru import logger

from document_categories.nosql_db_document_categories.repository_document import RepositoryDocument
from document_categories.vectordb_document_categories.cleaned_documents.cleaned_repository_document import CleanedRepositoryDocument

from data_preprocessors.data_cleaners.base.data_cleaner import DataCleaner

from utils.extension_to_programming_language import ExtensionToProgrammingLanguage

from settings import Settings


class RepositoryDataCleaner(DataCleaner):
    #Removing Comments from the programming content:
    def remove_python_like_comments(self,content:str) -> str:
        content=re.sub(r"#.*","",content,flags=re.MULTILINE)
        content=re.sub(r"'''.*'''","",content,flags=re.DOTALL)
        content=re.sub(r'""".*"""','',content,flags=re.DOTALL)


        return content


    def remove_c_like_comments(self,content:str) -> str:
        content=re.sub(r"//.*","",content,flags=re.MULTILINE)
        content=re.sub(r"/\*.*\*/","",content,flags=re.DOTALL)

        return content


    def remove_html_comments(self,content:str) -> str:
        content=re.sub(r"<!--.*-->","",content,flags=re.DOTALL)

        return content


    def remove_php_comments(self,content:str) -> str:
        content=re.sub(r"//.*","",content,flags=re.MULTILINE)
        content=re.sub(r"#.*","",content,flags=re.MULTILINE)
        content=re.sub(r"/\*.*\*/","",content,flags=re.DOTALL)

        return content


    def remove_ruby_comments(self,content:str) -> str:
        content=re.sub(r"#.*","",content,flags=re.MULTILINE)
        content=re.sub(r"=begin.*=end","",content,flags=re.DOTALL)

        return content


    def remove_julia_comments(self,content:str) -> str:
        content=re.sub(r"#=.*=#","",content,flags=re.DOTALL)
        content=re.sub(r"#.*","",content,flags=re.MULTILINE)
        content=re.sub(r'""".*"""','',content,flags=re.DOTALL)

        return content


    def remove_matlab_like_comments(self,content:str) -> str:
        content=re.sub(r"%\{.*%}","",content,flags=re.DOTALL)
        content=re.sub(r"%.*","",content,flags=re.MULTILINE)

        return content


    def remove_shell_comments(self,content:str) -> str:
        content=re.sub(r"^(?!#!)#.*$","",content,flags=re.MULTILINE)

        return content


    def remove_powershell_comments(self,content:str) -> str:
        content=re.sub(r"<#.*#>","",content,flags=re.DOTALL)
        content=re.sub(r"#.*","",content,flags=re.MULTILINE)

        return content


    def remove_sql_comments(self,content:str) -> str:
        content=re.sub(r"--.*","",content,flags=re.MULTILINE)
        content=re.sub(r"#.*","",content,flags=re.MULTILINE)
        content=re.sub(r"/\*.*\*/","",content,flags=re.DOTALL)

        return content


    def remove_lua_comments(self,content:str) -> str:
        content=re.sub(r"--\[\[.*]]","",content,flags=re.DOTALL)
        content=re.sub(r"--.*","",content,flags=re.MULTILINE)

        return content


    def remove_haskell_comments(self,content:str) -> str:
        content=re.sub(r"\{-.*-}","",content,flags=re.DOTALL)
        content=re.sub(r"--.*","",content,flags=re.MULTILINE)

        return content


    def remove_elixir_comments(self,content:str) -> str:
        content=re.sub(r"#.*","",content,flags=re.MULTILINE)
        content=re.sub(r'@moduledoc\s""".*"""','',content,flags=re.DOTALL)
        content = re.sub(r'@doc\s""".*"""','',content,flags=re.DOTALL)

        return content


    def remove_clojure_comments(self,content:str) -> str:
        content=re.sub(r";.*","",content,flags=re.MULTILINE)

        return content



    def clean(self,document_model:RepositoryDocument,minimum_content_length:int) -> CleanedRepositoryDocument|list[CleanedRepositoryDocument]|None:
        content=document_model.content
        repository_name=document_model.repository_name
        link=document_model.link

        if repository_name:
            repository_name=repository_name.strip()

        else:
            logger.info("No repository name exists.")
            repository_name="No repository name exists."


        if link:
            domains=Settings.REPOSITORY_DOMAINS
            if self.is_valid_link(link=link,domains=domains):
                pass

            else:
                logger.info("Invalid Link found.")
                link="No link exists."

        else:
            logger.info("No link exists.")
            link="No link exists."


        cleaned_files=0
        cleaned_repositories=[]
        for file_name,file_content in content.items():
            file_extension=file_name.split(".")[-1]
            programming_lang=ExtensionToProgrammingLanguage(extension=file_extension)

            #Removing comments from the content:
            if programming_lang in ["Python","YAML","TOML","CMAKE","R"]:
                cleaned_content=self.remove_python_like_comments(content=file_content)

            elif programming_lang in ["MATLAB","PERL"]:
                cleaned_content=self.remove_matlab_like_comments(content=file_content)

            elif programming_lang=="PHP":
                cleaned_content=self.remove_php_comments(content=file_content)

            elif programming_lang=="HTML":
                cleaned_content=self.remove_html_comments(content=file_content)

            elif programming_lang=="Ruby":
                cleaned_content=self.remove_ruby_comments(content=file_content)

            elif programming_lang=="Julia":
                cleaned_content=self.remove_julia_comments(content=file_content)

            elif programming_lang=="PowerShell":
                cleaned_content=self.remove_powershell_comments(content=file_content)

            elif programming_lang=="SQL":
                cleaned_content=self.remove_sql_comments(content=file_content)

            elif programming_lang=="Lua":
                cleaned_content=self.remove_lua_comments(content=file_content)

            elif programming_lang=="Haskell":
                cleaned_content=self.remove_haskell_comments(content=file_content)

            elif programming_lang=="Elixir":
                cleaned_content=self.remove_elixir_comments(content=file_content)

            else:
                cleaned_content=self.remove_c_like_comments(content=file_content)


            #Removing leading and trailing new line characters:
            cleaned_content=cleaned_content.strip("\n")

            cleaned_content_length=self.get_content_length(content=cleaned_content)
            if cleaned_content_length<minimum_content_length:
                logger.info("The length of the content is less than minimum content length.")
                continue

            else:
                cleaned_repo=CleanedRepositoryDocument(
                    content=cleaned_content,
                    platform=document_model.platform,
                    author_id=document_model.author_id,
                    author_full_name=document_model.author_full_name,
                    repository_name=repository_name,
                    link=link,
                    file_name=file_name,
                    programming_language_used=programming_lang
                )

                cleaned_repositories.append(cleaned_repo)
                cleaned_files+=1


        if cleaned_files==0:
            repo_name=document_model.repository_name
            logger.info(f"Every file in the repository: {repo_name} has length less than minimum content length.")
            logger.info("Therefore no file is cleaned.")

            return None

        else:
            file_count=document_model.file_count
            repo_name = document_model.repository_name
            logger.info(f"{cleaned_files}/{file_count} files in the repository: {repo_name} are cleaned successfully")

            if cleaned_files==1:
                return cleaned_repositories[0]

            else:
                return cleaned_repositories


