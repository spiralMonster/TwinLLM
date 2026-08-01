from document_categories.instruction_answer_document_categories.base.instruction_answer_document import InstructionAnswerDocument
from document_categories.data_category import DataCategory


class TweetInstructionAnswerDocument(InstructionAnswerDocument):
    class Config:
        data_category=DataCategory.TWEETS