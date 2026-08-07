from typing import Any


def get_metadata(
        deduplicating_metadata:dict[str,Any],
        additional_metadata_key:str|None=None,
        additional_metadata:dict[str,Any]|None=None
) -> dict[str,Any]:
    
    metadata={
        "num_instances_before_deduplication":deduplicating_metadata["num_instances_before_deduplication"],
        "num_instances_after_deduplication":deduplicating_metadata["num_instances_after_deduplication"],
        "num_instances_deduplicated":deduplicating_metadata["num_instances_before_deduplication"]-deduplicating_metadata["num_instances_after_deduplication"]
    }

    if additional_metadata_key:
        metadata[additional_metadata_key]=additional_metadata

    return metadata