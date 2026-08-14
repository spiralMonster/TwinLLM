from loguru import logger

from document_categories.vectordb_document_categories.embedded_documents.embedded_article_document import EmbeddedArticleDocument
from rag.prompt_creation.prompt_crafting.craft_from.base.craft_prompt import CraftPrompt


class CraftPromptFromArticles(CraftPrompt):
    @staticmethod
    def craft_prompt(documents:list[EmbeddedArticleDocument]) -> str:
        logger.info("Crafting Prompts from Articles.")

        prompts=[]
        info_prompt="## Context Gathered from Articles:"
        prompts.append(info_prompt)

        for doc in documents:
            prompt=f"""
            Content:
            {doc.content}
            Metadata:
             - Platform: {doc.platform}
             - Title: {doc.title}
             - Description: {doc.description}
             - Published Date: {doc.published_date}
            """

            prompts.append(prompt)

        prompts="\n".join(prompts)
        prompts=prompts.strip("\n")

        return prompts