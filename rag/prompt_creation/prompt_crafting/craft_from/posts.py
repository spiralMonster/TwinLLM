from loguru import logger

from document_categories.vectordb_document_categories.embedded_documents.embedded_post_document import EmbeddedPostDocument
from rag.prompt_creation.prompt_crafting.craft_from.base.craft_prompt import CraftPrompt


class CraftPromptFromPosts(CraftPrompt):
    @staticmethod
    def craft_prompt(documents:list[EmbeddedPostDocument]) -> str:
        logger.info("Crafting Prompts from Posts.")

        prompts=[]
        info_prompt="##Context Gathered from Posts:"
        prompts.append(info_prompt)

        for doc in documents:
            prompt=f"""
            Content:
            {doc.content}
            Metadata:
             - Platform: {doc.platform}
             - Published Date: {doc.published_date}
            """

            prompts.append(prompt)

        prompts="\n".join(prompts)
        prompts=prompts.strip("\n")

        return prompts