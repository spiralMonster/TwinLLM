from document_categories.instruction_answer_document_categories.base.instruction_answer_document import InstructionAnswerDocument

MAX_TOKEN_LENGTH=10000
MIN_TOKEN_LENGTH=0


def get_metadata(documents:list[InstructionAnswerDocument]) -> dict:
    metadata=dict()
    metadata["total_instruction_answer_pair"]=len(documents)

    for doc in documents:
        data_category=doc.get_category()
        instruction=doc.instruction
        answer=doc.answer

        metadata[data_category]["num_instruction_answer_pair"]=(
            metadata[data_category].get("num_instruction_answer_pair",0)+1
        )

        if data_category not in metadata:
            metadata[data_category]={
                "instructions":dict(),
                "answers":dict()
            }


        len_instruction=len(instruction.split(" "))
        metadata[data_category]["instructions"]["mean length (in tokens)"]=(
            metadata[data_category]["instructions"].get("mean length (in tokens)",len_instruction)+
            len_instruction
        )//2
        metadata[data_category]["instructions"]["max length (in tokens)"]=max(
            metadata[data_category]["instructions"].get("max length (in tokens)",MIN_TOKEN_LENGTH),
            len_instruction
        )
        metadata[data_category]["instructions"]["min length (in tokens)"]=min(
            metadata[data_category]["instructions"].get("min length (in tokens)",MAX_TOKEN_LENGTH),
            len_instruction
        )

        len_answer=len(answer.split(" "))
        metadata[data_category]["answers"]["mean length (in tokens)"]=(
            metadata[data_category]["answers"].get("mean length (in tokens)",len_answer)+
            len_answer
        )//2
        metadata[data_category]["answers"]["max length (in tokens)"]=max(
            metadata[data_category]["answers"].get("max length (in tokens)",MIN_TOKEN_LENGTH),
            len_answer
        )
        metadata[data_category]["answers"]["min length (in tokens)"]=min(
            metadata[data_category]["answers"].get("min length (in tokens)",MAX_TOKEN_LENGTH),
            len_answer
        )



    return metadata
