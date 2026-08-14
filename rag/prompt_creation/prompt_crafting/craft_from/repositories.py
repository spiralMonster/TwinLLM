from loguru import logger

from document_categories.vectordb_document_categories.embedded_documents.embedded_repository_document import EmbeddedRepositoryDocument
from rag.prompt_creation.prompt_crafting.craft_from.base.craft_prompt import CraftPrompt


class CraftPromptFromRepositories(CraftPrompt):
    @staticmethod
    def craft_prompt(documents:list[EmbeddedRepositoryDocument]) -> str:
        logger.info("Crafting Prompts from Code Repositories.")

        prompts=[]
        initial_prompt="## Context Gathered from Code Repositories:"
        prompts.append(initial_prompt)
    
        for doc in documents:
            prompt=f"""
            Content:
            {doc.content}
            Metadata:
             - Platform: {doc.platform}
             - Repository Name: {doc.repository_name}
             - File Name: {doc.file_name}
             - Programming languages used: {doc.programming_language_used}
            """
    
            prompts.append(prompt)
    
        prompts="\n".join(prompts)
        prompts=prompts.strip("\n")
    
        return prompts