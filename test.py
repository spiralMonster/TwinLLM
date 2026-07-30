from document_categories.nosql_db_document_categories.base.user_document import UserDocument
from document_categories.nosql_db_document_categories.repository_document import RepositoryDocument

from data_preprocessors.data_cleaners.repository_data_cleaner import RepositoryDataCleaner
import re
from langchain_text_splitters import RecursiveCharacterTextSplitter

if __name__=="__main__":
    user=UserDocument(
        first_name="Amartya",
        last_name="Pawar"
    )
    content={}

    with open("train.py","r",encoding="utf-8",errors="ignore") as file:
        content["train.py"]=file.read()


    repo_doc=RepositoryDocument(
        content=content,
        platform="Github",
        author_id=user.id,
        author_full_name=user.full_name,
        link="https://github.com"

    )

    # print(f"Length of repo document before cleaning: {len(repo_doc.content['train.py'])}")
    # print("Repo document before cleaning: ")
    # print(repo_doc.content['train.py'])
    #
    cleaned_doc=RepositoryDataCleaner().clean(document_model=repo_doc)
    #
    # print(f"Length of repo document after cleaning: {len(cleaned_doc.content)}")
    # print("Repo document after cleaning:")
    # print(cleaned_doc.content)

    chunked_docs=re.split(r"\n\n+",cleaned_doc.content)

    final_chunks=[]
    maximum_chunk_size=1000
    minimum_chunk_size=250
    character_splitter=RecursiveCharacterTextSplitter(
        chunk_size=maximum_chunk_size,
        chunk_overlap=0
    )
    for chunk in chunked_docs:
        if len(chunk)<=maximum_chunk_size:
            if len(chunk)>=minimum_chunk_size:
                chunk=chunk.strip()
                chunk=chunk.strip(r"\n")
                final_chunks.append(chunk)

        else:
            splitted_chunk=character_splitter.split_text(chunk)
            for c in splitted_chunk:
                if len(c)>=minimum_chunk_size:
                    chunk=chunk.strip()
                    chunk=chunk.strip(r"\n")

                    final_chunks.append(c)


    for ind,chunk in enumerate(final_chunks):
        print(f"Chunk: {ind+1}")
        print(f"Chunk length: {len(chunk)}")
        print("Content:")
        print(chunk)
        print(50*"-")
