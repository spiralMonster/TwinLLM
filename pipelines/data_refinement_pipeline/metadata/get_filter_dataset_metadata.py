from typing import Any

def get_metadata(
        filtering_metadata:dict[str,Any],
        instruction_filters:dict[str,Any],
        output_filters:dict[str,Any]
) -> dict[str,Any]:

    metadata={
        "num_instances_before_filtering":filtering_metadata["num_instances_before_filtering"],
        "num_instances_after_filtering":filtering_metadata["num_instances_after_filtering"],
        "num_instances_filtered":filtering_metadata["num_instances_before_filtering"]-filtering_metadata["num_instances_after_filtering"],
        "instructions_filtering":{
            "num_instructions_filtered":filtering_metadata["num_instructions_filtered"],
            "filtering_arguments":instruction_filters
        },
        "outputs_filtering":{
            "num_outputs_filtered":filtering_metadata["num_outputs_filtered"],
            "filtering_arguments":output_filters
        }
    }

    return metadata