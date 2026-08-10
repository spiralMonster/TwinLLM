from loguru import logger

from document_categories.vectordb_document_categories.chunked_documents.article_chunked_document import ArticleChunkedDocument
from document_categories.preference_dataset_document_categories.preference_document_from_article import PreferenceDocumentFromArticle

from dataset_generator.preference_dataset_generator.base.preference_dataset_generator import PreferenceDatasetGenerator

from utils.exceptions.model_exceptions.preference_dataset_generator_exception import PreferenceDatasetGeneratorException
from settings import Settings


class PreferenceDatasetGeneratorFromArticles(PreferenceDatasetGenerator):
    def generate(self,chunked_documents:list[ArticleChunkedDocument]) -> list[PreferenceDocumentFromArticle]:
        data_type="article"
        data_chunks=[
            doc.content for doc in chunked_documents
        ]

        temperature=Settings.TEMPERATURE_FOR_PREFERENCE_DATASET_GEN
        max_retries=Settings.MAX_RETRIES_FOR_PREFERENCE_DATASET_GEN

        models=[
            self.initialize_mistral_model(
                api_key=Settings.MISTRAL_API_KEY1_FOR_PREFERENCE_DATASET_GEN,
                temperature=temperature,
                max_retries=max_retries
            ),
            self.initialize_cohere_model(
                api_key=Settings.COHERE_API_KEY1_FOR_PREFERENCE_DATASET_GEN,
                temperature=temperature,
                max_retries=max_retries
            ),
            self.initialize_groq_model(
                api_key=Settings.GROQ_API_KEY1_FOR_PREFERENCE_DATASET_GEN,
                temperature=temperature,
                max_retries=max_retries
            ),
            self.initialize_qwen_model(
                api_key=Settings.GWEN_API_KEY1_FOR_PREFERENCE_DATASET_GEN,
                temperature=temperature,
                max_retries=max_retries
            )
        ]

        instructions,chosen_answers,rejected_answers=self.generate_preference_dataset(
            models=models,
            data_type=data_type,
            data_chunks=data_chunks
        )
        len_dataset=len(instructions)
        if len_dataset:
            preference_documents=[]
            for instruct,chosen_ans,rejected_ans in zip(instructions,chosen_answers,rejected_answers):
                doc=PreferenceDocumentFromArticle(
                    instruction=instruct,
                    chosen_answer=chosen_ans,
                    rejected_answer=rejected_ans
                )

                preference_documents.append(doc)


            return preference_documents

        else:
            logger.info("Failed to generate preference dataset from the Article Chunks.")
            raise PreferenceDatasetGeneratorException("Failed to generate the Preference dataset.")

