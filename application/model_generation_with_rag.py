from application.call_llm_service import call_llm_service

from rag.prompt_creation.create_prompt import CreatePrompt
from rag.post_generation_steps.conversation_history_handler import ConversationHistoryHandler
from rag.post_generation_steps.conversation_summary_handler import ConversationSummaryHandler


def generate(query:str) -> str:
    prompt_creator=CreatePrompt()
    prompt=prompt_creator.create(query=query)

    model_generation=call_llm_service(prompt=prompt)

    history_handler=ConversationHistoryHandler()
    history_handler.save_conversation(
        user_content=query,
        model_content=model_generation
    )

    summary_handler=ConversationSummaryHandler()
    summary_handler.save_summary(
        user_content=query,
        model_content=model_generation
    )

    return model_generation