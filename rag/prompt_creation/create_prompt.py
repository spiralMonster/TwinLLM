from opik import track

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
        Below is an instruction that describes a task.Write a response that appropriately completes the request.
        
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


    @track
    def create(self,query:str) -> str:
        print("[INFO] Building Prompt.")

        reconstructed_query,retrieved_documents=self.context_retriever.retrieve(
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
        reconstructed_query,
            context_crafted,
            conversation_history,
            conversation_summary,
            ''
        )
        final_prompt=final_prompt.strip()
        final_prompt=final_prompt.strip("\n")

        print("[INFO] Prompt build successfully.")

        return final_prompt



if __name__=="__main__":
    from loguru import logger
    logger.info("Building Prompt...")

    query="Hey, I am Raj Shamani, can you write an article about how the genz are different and what things they are doing differently?"
    prompt_creator=CreatePrompt()

    prompt=prompt_creator.create(query=query)
    logger.info("Prompt:")
    print(prompt)

    logger.info("Prompt build successfully.")

    #Demo Model Response
    model_response="In the rapidly evolving field of Natural Language Processing (NLP), fine-tuning has emerged as a powerful and effective technique to adapt pre-trained Large Language Models (LLMs) to specific downstream tasks. Pre-trained large-scale language models (as GPT family) have shown significant advancements in language understanding and generation. However, these pre-trained models are typically trained on vast amounts of text data with unsupervised learning and may not be optimized for a specific task."

    history_handler=ConversationHistoryHandler()
    summary_handler=ConversationSummaryHandler()

    history_handler.save_conversation(user_content=query,model_content=model_response)
    summary_handler.save_summary(user_content=query,model_content=model_response)











