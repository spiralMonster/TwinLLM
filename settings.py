from pydantic_settings import BaseSettings,SettingsConfigDict
from typing import Any


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
    EMBEDDING_MODEL_ID:str="sentence-transformers/all-MiniLM-L6-v2"
    EMBEDDING_MODEL_DEVICE:str="cpu"


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

    #Data Refinement Pipeline Parameters:
    INSTRUCTION_KEY:str="instructions"
    OUTPUT_KEY:str="outputs"

    ## Data Filtering Step Arguments:
    INSTRUCTION_LENGTH_BASED_FILTERS:dict[str,Any]={
        "min_length":6,
        "max_length":35
    }
    OUTPUT_LENGTH_BASED_FILTERS:dict[str,Any]={
        "min_length":15,
        "max_length":200
    }
    
    INSTRUCTION_TOXICITY_BASED_FILTERS:dict[str,Any]={
        "maximum_toxicity_threshold":0.75
    }
    OUTPUT_TOXICITY_BASED_FILTERS:dict[str,Any]={
        "maximum_toxicity_threshold":0.75
    }

    INSTRUCTION_FORMAT_BASED_FILTERS:dict[str,Any]={
        "start_with_capital":True,
        "end_with_punctuation":True
    }
    OUTPUT_FORMAT_BASED_FILTERS:dict[str,Any]={
        "start_with_capital":True,
        "end_with_punctuation":True
    }

    ###Toxicity Detection Model Settings:
    TOXICITY_DETECTION_MODEL_ID: str = "unitary/toxic-bert"
    TOXICITY_DETECTION_MODEL_DEVICE: str = "cpu"
    TOXICITY_DETECTION_MODEL_BATCH_SIZE: int = 32
    

    ## Data Deduplication Arguments:
    FUZZY_DEDUPLICATION_ARGUMENTS:dict[str,Any]={
        "algorithm":"MIN-HASH",
        "shingle_length":10,
        "number_of_hashes_per_document":128,
        "similarity_measure":"Jaccard Similarity",
        "minimimum_similarity_threshold":0.85
    }

    SEMANTIC_DEDUPLICATION_ARGUMENTS:dict[str,Any]={
        "EMBEDDING_MODEL":"sentence-transformers/all-MiniLM-L6-v2",
        "EMBEDDING_MODEL_DIM":384,
        "EMBEDDING_DATABASE":"HNSW",
        "similarity_measure":"cosine similarity",
        "minimum_cosine_similarity_threshold":0.75
    }
    
    ## DATA QUALITY EVALUATION SETTINGS:

    ### LLM As Judge Used for Data Quality Evaluation:
    LLM_JUDGE_FOR_DATA_QUALITY_EVALUATION: str = "mistral-medium-latest"
    LLM_JUDGE_FOR_DATA_QUALITY_EVALUATION_API_KEY:str
    LLM_JUDGE_FOR_DATA_QUALITY_EVALUATION_TEMP: float = 0.3
    LLM_JUDGE_FOR_DATA_QUALITY_EVALUATION_MAX_RETRIES: int = 3

    ### EVALUATION_METRICS_USED:
    DATA_QUALITY_EVALUATION_METRICS:list[str]=[
        "Helpfulness",
        "Correctness",
        "Coherence",
        "Complexity",
        "Relevance",
        "Verbosity"
    ]

    DATA_QUALITY_EVALUATION_MIN_SCORE_POSSIBLE_PER_METRIC:int=1
    DATA_QUALITY_EVALUATION_MAX_SCORE_POSSIBLE_PER_METRIC:int=5

    DATA_QUALITY_MINIMUM_SCORE_THRESHOLD:int=12

    # EVALUATED INSTRUCT DATASET NAME:
    EVALUATED_INSTRUCT_DATASET_NAME:str="llm_twin_instruct_evaluated_dataset"

    # CLEANED INSTRUCT DATASET NAME:
    CLEANED_INSTRUCT_DATASET_NAME:str="llm_twin_instruct_cleaned_dataset"

    COMET_API_KEY:str

    
    


Settings=SettingsClass()
