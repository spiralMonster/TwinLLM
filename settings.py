from pydantic_settings import BaseSettings,SettingsConfigDict


class SettingsClass(BaseSettings):
    model_config=SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8"
    )

    #Mongodb Configs:
    MONGODB_DATABASE_HOST: str
    MONGODB_DATABASE_NAME: str

    #Qdrant Configs:
    USE_QDRANT_CLOUD:bool
    QDRANT_API_KEY: str
    QDRANT_CLOUD_URL:str

    QDRANT_DATABASE_HOST:str = "localhost"
    QDRANT_DATABASE_PORT:int = 6333


    #Embedding Model Configs:
    EMBEDDING_MODEL_ID:str = "sentence-transformers/all-MiniLM-L6-v2"
    EMBEDDING_MODEL_DEVICE:str = "cpu"


    #LinkedIn Credentials:
    LINKEDIN_USERNAME:str
    LINKEDIN_PASSWORD:str

    #Thread Credentials:
    THREADS_USERNAME:str
    THREADS_PASSWORD:str

    #AWS Credentials:
    AWS_REGION:str
    AWS_ACCESS_KEY:str
    AWS_SECRET_KEY:str

    #Post Domains:
    POST_DOMAINS:list[str]=["https://linkedin.com"]

    #Article Domains:
    ARTICLE_DOMAINS:list[str]=["https://medium.com","https://substack.com"]

    #Repository Domains:
    REPOSITORY_DOMAINS:list[str]=["https://github.com"]

    #Tweet Domains:
    TWEET_DOMAINS:list[str]=["https://x.com","https://threads.com"]


Settings=SettingsClass()
