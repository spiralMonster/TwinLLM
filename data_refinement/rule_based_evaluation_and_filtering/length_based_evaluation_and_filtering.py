from typing import Any
from datasets import Dataset

def filtering_based_on_content_length(
        example:dict[str,Any],
        filtering_key:str,
        min_length:int,
        max_length:int
) -> bool:

    content=example[filtering_key]
    content_length=len(content.split())

    result=(content_length>=min_length) and (content_length<=max_length)

    return result



def length_based_filtering(
        dataset:Dataset,
        instruction_key:str,
        output_key:str,
        instruction_filters:dict[str,Any],
        output_filters:dict[str,Any]
) -> Dataset:

    print(50 * "-")
    print("[START] Filtering the Dataset based on Content Length.")
    initial_num_instances=len(dataset)

    print("[INFO] Filtering the Dataset based on Instructions Length.")
    print("[INFO] Filtering arguments received:")
    print(instruction_filters)
    
    print(f"[INFO] Total number of instances before Instructions Length Based Filtering: {len(dataset)}")
    dataset=dataset.filter(
        filtering_based_on_content_length,
        fn_kwargs={
            "filtering_key":instruction_key,
            "min_length":instruction_filters["min_length"],
            "max_length":instruction_filters["max_length"]
        }
    )
    print(f"[INFO] Total number of instances after Instructions Length Based Filtering: {len(dataset)}")
    
    
    print("[INFO] Filtering the Dataset based on Outputs Length.")
    print("[INFO] Filtering arguments received:")
    print(output_filters)

    print(f"[INFO] Total number of instances before Outputs Length Based Filtering: {len(dataset)}")
    dataset=dataset.filter(
        filtering_based_on_content_length,
        fn_kwargs={
            "filtering_key":output_key,
            "min_length":output_filters["min_length"],
            "max_length":output_filters["max_length"]
        }
    )
    print(f"[INFO] Total number of instances after Outputs Length Based Filtering: {len(dataset)}")


    print(f"[INFO] Total number of instances before Length Based Filtering: {initial_num_instances}")
    print(f"[INFO] Total number of instances after Length Based Filtering: {len(dataset)}")

    print("[END] Filtering the Dataset based on Content Length.")
    print(50 * "-")

    return dataset



def length_based_evaluation(
        dataset:Dataset,
        instruction_key:str,
        output_key:str
) -> Dataset:

    instruction_length_key=f"{instruction_key}_length"
    output_length_key=f"{output_key}_length"

    dataset=dataset.map(
        lambda example:{
            instruction_length_key:len(example[instruction_key].split()),
            output_length_key:len(example[output_key].split())
        }
    )

    print("[INFO] Dataset Evaluated Based On Content Length.")
    return dataset



def length_based_evaluation_and_filtering(
        evaluated_dataset:Dataset,
        cleaned_dataset:Dataset,
        instruction_key:str,
        output_key:str,
        instruction_filters:dict[str,Any],
        output_filters:dict[str,Any],
        create_evaluation_dataset:bool=True,
        filter_dataset:bool=True
) -> tuple[Dataset,Dataset]:

    if create_evaluation_dataset:
        evaluated_dataset=length_based_evaluation(
            dataset=evaluated_dataset,
            instruction_key=instruction_key,
            output_key=output_key
        )


    if filter_dataset:
        cleaned_dataset=length_based_filtering(
            dataset=cleaned_dataset,
            instruction_key=instruction_key,
            output_key=output_key,
            instruction_filters=instruction_filters,
            output_filters=output_filters
        )



    return evaluated_dataset,cleaned_dataset



    
