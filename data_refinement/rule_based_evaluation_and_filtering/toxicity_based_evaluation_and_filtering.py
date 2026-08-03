from typing import Any
from datasets import Dataset

from models.toxicity_detection_model import ToxicityDetectionModel
from settings import Settings


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

    texts=list(example_batches[filtering_key])
    toxicity_results=generate_text_toxicity_result(texts=texts)

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

    print(50*"-")
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
    print(50*"-")

    return dataset



def toxicity_based_evaluation(
        dataset:Dataset,
        instruction_key:str,
        output_key:str
) -> Dataset:

    instruction_toxicity_result_key=f"{instruction_key}_toxicity_results"
    output_toxicity_result_key=f"{output_key}_toxicity_results"

    dataset=dataset.map(
        lambda example_batches:{
            instruction_toxicity_result_key:generate_text_toxicity_result(
                texts=list(example_batches[instruction_key])
            ),
            output_toxicity_result_key:generate_text_toxicity_result(
                texts=list(example_batches[output_key])
            )
        },
        batched=True,
        batch_size=toxicity_detection_model_batch_size
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

    if create_evaluation_dataset:
        evaluated_dataset=toxicity_based_evaluation(
            dataset=evaluated_dataset,
            instruction_key=instruction_key,
            output_key=output_key
        )

    if filter_dataset:
        cleaned_dataset=toxicity_based_filtering(
            dataset=cleaned_dataset,
            instruction_key=instruction_key,
            output_key=output_key,
            instruction_filters=instruction_filters,
            output_filters=output_filters
        )


    return evaluated_dataset,cleaned_dataset