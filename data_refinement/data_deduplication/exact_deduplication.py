from datasets import Dataset
from typing import Any


def filter_duplicates(
        example:dict[str,Any],
        instruction_key:str,
        output_key:str,
        visited_examples:set[tuple[str,str]]
) -> bool:
    instruction=example[instruction_key]
    output=example[output_key]

    key=(instruction,output)

    if key in visited_examples:
        return False

    visited_examples.add(key)
    return True



def exact_deduplication(
        dataset:Dataset,
        instruction_key:str,
        output_key:str,
) -> Dataset:

    print("[START] Exact Deduplication of instances in the Dataset.")
    initial_num_instances=len(dataset)

    visited_examples=set()
    dataset=dataset.filter(
        filter_duplicates,
        fn_kwargs={
            "instruction_key":instruction_key,
            "output_key":output_key,
            "visited_examples":visited_examples
        }
    )

    print(f"[INFO] Total number of instances before Exact Data Deduplication: {initial_num_instances}")
    print(f"[INFO] Total number of instances after Exact Data Deduplication: {len(dataset)}")

    return dataset
    

    
        
        
        
        
        
