from loguru import logger
from document_categories.rag_document_categories.conversation_history_document import ConversationHistoryDocument

class ConversationHistoryHandler:
    @staticmethod
    def save_conversation(user_content:str,model_content:str) -> bool:
        content=f"""
        User:
        {user_content}
        Model:
        {model_content}
        """

        conversation_document=ConversationHistoryDocument(
            conversation=content
        )

        result=ConversationHistoryDocument.bulk_insert(documents=[conversation_document])

        logger.info("Conversation saved successfully.")
        return result

    @staticmethod
    def retrieve_conversations(num_conversation_to_retrieve:int) -> str:
        num_conversation=ConversationHistoryDocument.get_num_points_in_collection()
        if num_conversation==0:
            return ""

        else:
            conversation_documents=ConversationHistoryDocument.get_latest_conversations(
                limit=num_conversation_to_retrieve
            )
            conversation_documents=reversed(conversation_documents)

            retrieved_conversations=[
                doc.conversation
                for doc in conversation_documents
            ]
            retrieved_conversations="\n".join(retrieved_conversations)
            retrieved_conversations=retrieved_conversations.strip("\n")

            logger.info("Conversations retrieved successfully.")
            return retrieved_conversations




if __name__=="__main__":
    logger.info("Retrieving the Conversation History:")

    history_handler=ConversationHistoryHandler()
    conversations=history_handler.retrieve_conversations(num_conversation_to_retrieve=1)

    logger.info("Retrieved Conversations: ")
    print(conversations)


