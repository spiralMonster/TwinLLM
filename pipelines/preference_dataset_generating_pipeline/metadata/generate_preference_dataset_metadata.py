from document_categories.preference_dataset_document_categories.base.preference_document import PreferenceDocument

MAX_TOKEN_LENGTH=10000
MIN_TOKEN_LENGTH=0

def get_metadata(documents:list[PreferenceDocument]) -> dict:
    metadata=dict()
    metadata["total_preference_triplets"]=len(documents)

    for doc in documents:
        data_category=doc.get_category()
        instruction=doc.instruction
        chosen_answer=doc.chosen_answer
        rejected_answer=doc.rejected_answer

        if data_category not in metadata:
            metadata[data_category]={
                "instructions":dict(),
                "chosen_answers":dict(),
                "rejected_answers":dict()
            }

        metadata[data_category]["num_preference_triplets"]=(
            metadata[data_category].get("num_preference_triplets",0)+1
        )

        len_instruction=len(instruction.split())
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
        
        len_chosen_answer=len(chosen_answer.split())
        metadata[data_category]["chosen_answers"]["mean length (in tokens)"]=(
            metadata[data_category]["chosen_answers"].get("mean length (in tokens)",len_chosen_answer)+
            len_chosen_answer
        )//2
        metadata[data_category]["chosen_answers"]["max length (in tokens)"]=max(
            metadata[data_category]["chosen_answers"].get("max length (in tokens)",MIN_TOKEN_LENGTH),
            len_chosen_answer
        )
        metadata[data_category]["chosen_answers"]["min length (in tokens)"]=min(
            metadata[data_category]["chosen_answers"].get("min length (in tokens)",MAX_TOKEN_LENGTH),
            len_chosen_answer
        )
        
        len_rejected_answer=len(rejected_answer.split())
        metadata[data_category]["rejected_answers"]["mean length (in tokens)"]=(
            metadata[data_category]["rejected_answers"].get("mean length (in tokens)",len_rejected_answer)+
            len_rejected_answer
        )//2
        metadata[data_category]["rejected_answers"]["max length (in tokens)"]=max(
            metadata[data_category]["rejected_answers"].get("max length (in tokens)",MIN_TOKEN_LENGTH),
            len_rejected_answer
        )
        metadata[data_category]["rejected_answers"]["min length (in tokens)"]=min(
            metadata[data_category]["rejected_answers"].get("min length (in tokens)",MAX_TOKEN_LENGTH),
            len_rejected_answer
        )


    return metadata
        
        
        
        
        
        
