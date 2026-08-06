from typing import Any
from datasets import Dataset

from data_refinement.data_quality_evaluation.using_llm_as_judge.utils.data_quality_evaluator import DataQualityEvaluator

data_quality_evaluator=DataQualityEvaluator()


def filtering_based_on_quality(
        example:dict[str,Any],
        filtering_key:str,
        minimum_score:int
) -> bool:
    result=example[filtering_key]
    if result:
        score=0
        for value in result.values():
            score+=value
        
        if score>=minimum_score:
            return True
        
        else:
            return False
    
    else:
        return True


def data_quality_based_filtering(
        dataset:Dataset,
        filtering_key:str,
        filters:dict[str,Any]
) -> Dataset:
    
    print("[START] Filtering Dataset based on Data Quality.")
    initial_num_instances=len(dataset)
    
    print("[INFO] Filtering arguments received: ")
    print(filters)
    
    dataset=dataset.filter(
        filtering_based_on_quality,
        fn_kwargs={
            "filtering_key":filtering_key,
            "minimum_score":filters["minimum_score"]
        }
    )
    
    print(f"[INFO] Total number of instances before filtering based on Data Quality: {initial_num_instances}")
    print(f"[INFO] Total number of instances after filtering based on Data Quality: {len(dataset)}")

    print("[END] Filtering Dataset based on Data Quality.")
    return dataset
    
    
    

def data_quality_based_evaluation(
        dataset:Dataset,
        filtering_key:str,
        results:list[dict[str,Any]]
) -> Dataset:
    
    dataset=dataset.add_column(
        filtering_key,
        results
    )
    
    print("[INFO] Dataset evaluated based on Data Quality.")
    return  dataset



def quality_based_evaluation_and_filtering(
        evaluated_dataset:Dataset,
        cleaned_dataset:Dataset,
        instruction_key:str,
        output_key:str,
        filters:dict[str,Any],
        create_evaluation_dataset:bool=True,
        filter_dataset:bool=True
) -> tuple[Dataset,Dataset]:

    print(25 * "-" + "START:Data Quality(Using LLM AS JUDGE) Based Filtering And Evaluation" + 25 * "-")

    if create_evaluation_dataset or filter_dataset:
        evaluated_dataset=evaluated_dataset.map(
            lambda example:{
                "instruction_output_pair":f"Instruction:\n{example[instruction_key]}\nOutput:\n{example[output_key]}"
            }
        )
        instruction_output_pairs=list(evaluated_dataset["instruction_output_pair"])
        
        evaluation_results=data_quality_evaluator.evaluate(
            instruction_output_pairs=instruction_output_pairs
        )
        
        evaluation_result_key="data_quality_evaluation_result"
        evaluated_dataset=data_quality_based_evaluation(
            dataset=evaluated_dataset,
            filtering_key=evaluation_result_key,
            results=evaluation_results
        )
        
        evaluated_dataset=evaluated_dataset.remove_columns(["instruction_output_pair"])
        
        if filter_dataset:
            lookup_table={
                row["id"]:{
                    evaluation_result_key:row[evaluation_result_key]
                }
                for row in evaluated_dataset
            }
            
            cleaned_dataset=cleaned_dataset.map(
                lambda example:lookup_table[example["id"]]
            )
            
            cleaned_dataset=data_quality_based_filtering(
                dataset=cleaned_dataset,
                filtering_key=evaluation_result_key,
                filters=filters
            )
            
            cleaned_dataset.remove_columns([
                evaluation_result_key
            ])
        
        
        if not create_evaluation_dataset:
            evaluated_dataset=evaluated_dataset.remove_columns([
                evaluation_result_key
            ])


    print(25 * "-" + "END:Data Quality(Using LLM AS JUDGE) Based Filtering And Evaluation:" + 25 * "-")
    return evaluated_dataset,cleaned_dataset
        
        
        