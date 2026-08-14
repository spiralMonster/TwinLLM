from document_categories.vectordb_document_categories.embedded_documents.base.embedded_document import EmbeddedDocument
from document_categories.data_category import DataCategory

from rag.prompt_creation.prompt_crafting.dispatcher.prompt_crafting_handler import PromptCraftingHandler


class PromptCraftingDispatcher:
    prompt_craft_handler=PromptCraftingHandler()

    @classmethod
    def dispatch(cls,embedded_documents:list[EmbeddedDocument]) -> str:
        doc=embedded_documents[0]

        category=doc.get_category()
        data_category=DataCategory(category)

        handler=cls.prompt_craft_handler.create_handler(data_category=data_category)

        crafted_prompts=handler.craft_prompt(documents=embedded_documents)
        return crafted_prompts



