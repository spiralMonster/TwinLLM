from rag.prompt_creation.context_retriever.retrieve_context import ContextRetriever
from rag.prompt_creation.prompt_crafting.craft import CraftPrompt

from rag.post_generation_steps.conversation_history_handler import ConversationHistoryHandler
from rag.post_generation_steps.conversation_summary_handler import ConversationSummaryHandler

from settings import Settings


class CreatePrompt:
    def __init__(self) -> None:
        self.context_retriever=ContextRetriever()
        self.prompt_crafter=CraftPrompt()
        self.conversation_history_handler=ConversationHistoryHandler()
        self.conversation_summary_handler=ConversationSummaryHandler()


    @staticmethod
    def generate_template() -> str:
        template="""
        ### Instruction:
        {}
        
        ### Context Gathered:
        {}
        
        ### Conversation History:
        {}
        
        ### Conversation Summary:
        {}
        
        ### Response:
        """

        return template


    def create(self,query:str) -> str:
        print("[INFO] Building Prompt.")

        retrieved_documents=self.context_retriever.retrieve(
            query=query
        )
        print("[INFO] Context Retrieved.")

        context_crafted=self.prompt_crafter.craft(documents=retrieved_documents)
        print("[INFO] Prompt Crafted.")

        conversation_history=self.conversation_history_handler.retrieve_conversations(
            num_conversation_to_retrieve=Settings.NUM_OF_CONVERSATION_TO_RETRIEVE
        )
        print("[INFO] Conversation History Retrieved.")

        conversation_summary=self.conversation_summary_handler.retrieve_summary()
        print("[INFO] Conversation Summary Retrieved.")

        prompt_temp=self.generate_template()

        final_prompt=prompt_temp.format(
            query,
            context_crafted,
            conversation_history,
            conversation_summary,
            ''
        )
        final_prompt=final_prompt.strip()
        final_prompt=final_prompt.strip("\n")

        print("[INFO] Prompt build successfully.")

        return final_prompt









