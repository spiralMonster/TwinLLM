from typing import Any
from datasets import Dataset


def filtering_based_on_format(
        example:dict[str,Any],
        filtering_key:str,
        start_with_capital:bool,
        end_with_punctuation:bool
) -> bool:
    text=example[filtering_key].strip()

    if start_with_capital:
        if end_with_punctuation:
            result=(text[0].isupper()) and (any(text[-1]==p for p in ".?!"))
            return result

        else:
            result=text[0].isupper()
            return result

    else:
        if end_with_punctuation:
            result=any(text[-1]==p for p in ".?!")
            return result

        else:
            return True



def format_based_filtering(
        dataset:Dataset,
        instruction_key:str,
        output_key:str,
        instruction_filters:dict[str,Any],
        output_filters:dict[str,Any]
) -> tuple[Dataset,dict[str,Any]]:

    metadata=dict()

    print("[START] Filtering the Dataset based on Format.")
    initial_num_instances=len(dataset)
    metadata["num_instances_before_filtering"]=initial_num_instances

    print("[INFO] Filtering the Dataset based on Instructions Format.")
    print("[INFO] Filtering Arguments received: ")
    print(instruction_filters)

    initial_num_instructions=initial_num_instances
    print(f"[INFO] Total number of instances before Instructions Format Based Filtering: {initial_num_instructions}")
    dataset=dataset.filter(
        filtering_based_on_format,
        fn_kwargs={
            "filtering_key":instruction_key,
            "start_with_capital":instruction_filters["start_with_capital"],
            "end_with_punctuation":instruction_filters["end_with_punctuation"]
        }
    )

    final_num_instruction=len(dataset)
    print(f"[INFO] Total number of instances after Instructions Format Based Filtering: {final_num_instruction}")
    metadata["num_instructions_filtered"]=initial_num_instructions-final_num_instruction


    print("[INFO] Filtering the Dataset based on Outputs Format.")
    print("[INFO] Filtering arguments received:")
    print(output_filters)
    
    initial_num_outputs=final_num_instruction
    print(f"[INFO] Total number of instances before Outputs Format Based Filtering: {initial_num_outputs}")
    dataset=dataset.filter(
        filtering_based_on_format,
        fn_kwargs={
            "filtering_key":output_key,
            "start_with_capital":output_filters["start_with_capital"],
            "end_with_punctuation":output_filters["end_with_punctuation"]
        }
    )

    final_num_outputs=len(dataset)
    print(f"[INFO] Total number of instances after Outputs Format Based Filtering: {final_num_outputs}")
    metadata["num_outputs_filtered"]=initial_num_outputs-final_num_outputs
    
    
    print(f"[INFO] Total number of instances before Format Based Filtering: {initial_num_instances}")
    print(f"[INFO] Total number of instances after Format Based Filtering: {final_num_outputs}")
    metadata["num_instances_after_filtering"]=final_num_outputs

    print("[END] Filtering the Dataset based on Format.")

    return dataset,metadata



def format_based_evaluation(
        dataset:Dataset,
        instruction_key:str,
        output_key:str,
        instruction_filters:dict[str,Any],
        output_filters:dict[str,Any]
) -> Dataset:

    instruction_format_satisfaction_key=f"{instruction_key}_satisfy_format"
    output_format_satisfaction_key=f"{output_key}_satisfy_format"

    dataset=dataset.map(
        lambda e:{
            instruction_format_satisfaction_key:"Yes" if filtering_based_on_format(
                example=e,
                filtering_key=instruction_key,
                start_with_capital=instruction_filters["start_with_capital"],
                end_with_punctuation=instruction_filters["end_with_punctuation"]
            ) else "No",

            output_format_satisfaction_key:"Yes" if filtering_based_on_format(
                example=e,
                filtering_key=output_key,
                start_with_capital=output_filters["start_with_capital"],
                end_with_punctuation=output_filters["end_with_punctuation"]
            ) else "No"

        }
    )

    print("[INFO] Dataset Evaluated Based on Format.")
    return dataset



def format_based_evaluation_and_filtering(
        evaluated_dataset:Dataset,
        cleaned_dataset:Dataset,
        instruction_key:str,
        output_key:str,
        instruction_filters:dict[str,Any],
        output_filters:dict[str,Any],
        create_evaluation_dataset:bool=True,
        filter_dataset:bool=True
) -> tuple[tuple[Dataset,Dataset],dict[str,Any]]:
    
    print(25 * "-" + "START:Format Based Filtering And Evaluation" + 25 * "-")
    metadata=dict()
    
    if create_evaluation_dataset:
        evaluated_dataset=format_based_evaluation(
            dataset=evaluated_dataset,
            instruction_key=instruction_key,
            output_key=output_key,
            instruction_filters=instruction_filters,
            output_filters=output_filters
        )


    if filter_dataset:
        cleaned_dataset,metadata=format_based_filtering(
            dataset=cleaned_dataset,
            instruction_key=instruction_key,
            output_key=output_key,
            instruction_filters=instruction_filters,
            output_filters=output_filters
        )

    print(25 * "-" + "END:Format Based Filtering And Evaluation" + 25 * "-")
    return (evaluated_dataset,cleaned_dataset),metadata
    
    
    



