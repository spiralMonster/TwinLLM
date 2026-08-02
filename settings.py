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

    #Hugging Face Token:
    HF_TOKEN:str
    HF_USERNAME:str

    #API KEYS FOR LLM Service Provider:
    MISTRAL_API_KEY:str
    COHERE_API_KEY:str
    GROQ_API_KEY:str
    QWEN_API_KEY:str

    #LLMs Used for Instruction-Answer Pair Generator:
    MISTRAL_MODEL:str="mistral-medium-latest"
    COHERE_MODEL:str="command-r-08-2024"
    GROQ_MODEL:str="llama-3.3-70b-versatile"
    QWEN_MODEL:str="qwen-flash"


    #Instruction-Answer Pair Generator Model Settings:
    INSTRUCT_ANS_GENERATOR_TEMP:float=0.6
    INSTRUCT_ANS_GENERATOR_MAX_RETRIES:int=3

    INSTRUCT_DATASET_NAME:str="llm_twin_instruct_dataset"
    
    #API KEYS FOR LLM USED FOR INSTRUCT DATASET GENERATION FROM ARTICLE_CHUNKS:
    MISTRAL_API_KEY1:str
    COHERE_API_KEY1:str
    GROQ_API_KEY1:str
    QWEN_API_KEY1:str

    #API KEYS FOR LLM USED FOR INSTRUCT DATASET GENERATION FROM POST_CHUNKS:
    MISTRAL_API_KEY2:str
    COHERE_API_KEY2:str
    GROQ_API_KEY2:str
    QWEN_API_KEY2:str

    #API KEYS FOR LLM USED FOR INSTRUCT DATASET GENERATION FROM REPOSITORY_CHUNKS:
    MISTRAL_API_KEY3:str
    COHERE_API_KEY3:str
    GROQ_API_KEY3:str
    QWEN_API_KEY3:str

    #API KEYS FOR LLM USED FOR INSTRUCT DATASET GENERATION FROM TWEET_CHUNKS:
    MISTRAL_API_KEY4:str
    COHERE_API_KEY4:str
    GROQ_API_KEY4:str
    QWEN_API_KEY4:str


Settings=SettingsClass()
