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
) -> tuple[Dataset,dict[str,Any]]:

    metadata=dict()

    print(25 * "-" + "START:EXACT DEDUPLICATION" + 25 * "-")
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

    final_num_instances=len(dataset)
    print(f"[INFO] Total number of instances before Exact Data Deduplication: {initial_num_instances}")
    print(f"[INFO] Total number of instances after Exact Data Deduplication: {final_num_instances}")

    metadata["num_instances_before_deduplication"]=initial_num_instances
    metadata["num_instances_after_deduplication"]=final_num_instances

    print(25 * "-" + "END:EXACT DEDUPLICATION" + 25 * "-")
    return dataset,metadata
    

        
        
        
        
