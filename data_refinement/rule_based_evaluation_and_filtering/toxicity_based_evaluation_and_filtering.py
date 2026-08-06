from typing import Any
from datasets import Dataset

from utils.batch_data import batch
from settings import Settings

from models.toxicity_detection_model import ToxicityDetectionModel


toxicity_detection_model_batch_size=Settings.TOXICITY_DETECTION_MODEL_BATCH_SIZE
toxicity_detection_model=ToxicityDetectionModel()


def generate_text_toxicity_result(texts:list[str]) -> list[dict[str,float]]:
    result=toxicity_detection_model(texts=texts)

    return result


def filtering_based_on_text_toxicity(
        example_batches:dict[str,list[Any]],
        filtering_key:str,
        maximum_toxicity_threshold:float
) -> list[bool]:

    toxicity_results=list(example_batches[filtering_key])
    toxicity_result_values=[
        list(result.values())
        for result in toxicity_results
    ]

    result=[
        all(value<maximum_toxicity_threshold for value in values)
        for values in toxicity_result_values
    ]

    return result


def toxicity_based_filtering(
        dataset:Dataset,
        instruction_key:str,
        output_key:str,
        instruction_filters:dict[str,Any],
        output_filters:dict[str,Any]
) -> Dataset:

    print("[START] Filtering the Dataset based on the Toxicity of the Text.")
    initial_num_instances=len(dataset)

    print("[INFO] Filtering the Dataset based on the Toxicity of Instructions.")
    print("[INFO] Filtering arguments received:")
    print(instruction_filters)

    print(f"[INFO] Total number of instances before Instructions Toxicity Based Filtering: {len(dataset)}")
    dataset=dataset.filter(
        filtering_based_on_text_toxicity,
        fn_kwargs={
            "filtering_key":instruction_key,
            "maximum_toxicity_threshold":instruction_filters["maximum_toxicity_threshold"]
        },
        batched=True,
        batch_size=toxicity_detection_model_batch_size
    )
    print(f"[INFO] Total number of instances after Instructions Toxicity Based Filtering: {len(dataset)}")


    print("[INFO] Filtering the Dataset based on the Toxicity of Outputs.")
    print("[INFO] Filtering arguments received:")
    print(output_filters)

    print(f"[INFO] Total number of instances before Outputs Toxicity Based Filtering: {len(dataset)}")
    dataset=dataset.filter(
        filtering_based_on_text_toxicity,
        fn_kwargs={
            "filtering_key":output_key,
            "maximum_toxicity_threshold":output_filters["maximum_toxicity_threshold"]
        },
        batched=True,
        batch_size=toxicity_detection_model_batch_size
    )
    print(f"[INFO] Total number of instances after Outputs Toxicity Based Filtering: {len(dataset)}")


    print(f"[INFO] Total number of instances before Toxicity Based Filtering: {initial_num_instances}")
    print(f"[INFO] Total number of instances after Toxicity Based Filtering: {len(dataset)}")

    print("[END] Filtering the Dataset based on the Toxicity of the Text.")

    return dataset



def toxicity_based_evaluation(
        dataset:Dataset,
        instruction_key:str,
        output_key:str,
        toxicity_result_for_instructions:list[dict[str,float]],
        toxicity_result_for_outputs:list[dict[str,float]]
) -> Dataset:
    
    instruction_toxicity_result_key=f"{instruction_key}_toxicity_results"
    output_toxicity_result_key=f"{output_key}_toxicity_results"

    dataset=dataset.add_column(
        instruction_toxicity_result_key,
        toxicity_result_for_instructions
    )
    dataset=dataset.add_column(
        output_toxicity_result_key,
        toxicity_result_for_outputs
    )

    print("[INFO] Dataset Evaluated Based on Text Toxicity.")
    return dataset



def toxicity_based_evaluation_and_filtering(
        evaluated_dataset:Dataset,
        cleaned_dataset:Dataset,
        instruction_key:str,
        output_key:str,
        instruction_filters:dict[str,Any],
        output_filters:dict[str,Any],
        create_evaluation_dataset:bool=True,
        filter_dataset:bool=True
) -> tuple[Dataset,Dataset]:

    print(25 * "-" + "START:Toxicity Based Filtering And Evaluation" + 25 * "-")

    if create_evaluation_dataset or filter_dataset:
        toxicity_result_for_instructions=[]
        toxicity_result_for_outputs=[]

        instructions=list(evaluated_dataset[instruction_key])

        instructions_batch=batch(instructions,batch_size=toxicity_detection_model_batch_size)
        for instruction_batch in instructions_batch:
            results=generate_text_toxicity_result(texts=instruction_batch)
            toxicity_result_for_instructions.extend(results)

        outputs=list(evaluated_dataset[output_key])
        outputs_batch=batch(outputs,batch_size=toxicity_detection_model_batch_size)
        for output_batch in outputs_batch:
            results=generate_text_toxicity_result(texts=output_batch)
            toxicity_result_for_outputs.extend(results)


        evaluated_dataset=toxicity_based_evaluation(
            dataset=evaluated_dataset,
            instruction_key=instruction_key,
            output_key=output_key,
            toxicity_result_for_instructions=toxicity_result_for_instructions,
            toxicity_result_for_outputs=toxicity_result_for_outputs
        )

        instruction_toxicity_result_key = f"{instruction_key}_toxicity_results"
        output_toxicity_result_key = f"{output_key}_toxicity_results"

        if filter_dataset:
            lookup_table={
                row["id"]:{
                   instruction_toxicity_result_key:row[instruction_toxicity_result_key],
                   output_toxicity_result_key:row[output_toxicity_result_key]

                }
                for row in evaluated_dataset
            }

            cleaned_dataset=cleaned_dataset.map(
                lambda example:lookup_table[example["id"]]
            )

            cleaned_dataset=toxicity_based_filtering(
                dataset=cleaned_dataset,
                instruction_key=instruction_toxicity_result_key,
                output_key=output_toxicity_result_key,
                instruction_filters=instruction_filters,
                output_filters=output_filters
            )

            cleaned_dataset=cleaned_dataset.remove_columns([
                instruction_toxicity_result_key,
                output_toxicity_result_key
            ])
        
        
        if not create_evaluation_dataset:
            evaluated_dataset=evaluated_dataset.remove_columns([
                instruction_toxicity_result_key,
                output_toxicity_result_key
            ])


    print(25 * "-" + "END:Toxicity Based Filtering And Evaluation" + 25 * "-")
    return evaluated_dataset,cleaned_dataset





