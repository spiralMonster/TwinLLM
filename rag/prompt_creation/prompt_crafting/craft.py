from document_categories.vectordb_document_categories.embedded_documents.base.embedded_document import EmbeddedDocument
from rag.prompt_creation.prompt_crafting.dispatcher.prompt_crafting_dispatcher import PromptCraftingDispatcher


class CraftPrompt:
    @staticmethod
    def craft(documents:list[EmbeddedDocument]) -> str:
        grouped_documents=EmbeddedDocument.group_by_class(documents)

        dispatcher=PromptCraftingDispatcher
        crafted_prompts=[]
        for document_class,docs in grouped_documents.items():
            prompt=dispatcher.dispatch(embedded_documents=docs)
            crafted_prompts.append(prompt)


        crafted_prompts="\n\n".join(crafted_prompts)
        crafted_prompts=crafted_prompts.strip("\n")

        return crafted_prompts
