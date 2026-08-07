from typing import Any
from settings import Settings

def get_metadata(
        num_instances_before_filtering:int,
        num_instances_after_filtering:int,
        mean_evaluation_score_given_by_llm_as_judge:int

) -> dict[str,Any]:

    metadata={
        "llm_as_judge_details":{
            "MODEL":Settings.LLM_JUDGE_FOR_DATA_QUALITY_EVALUATION,
            "TEMPERATURE":Settings.LLM_JUDGE_FOR_DATA_QUALITY_EVALUATION_TEMP,
            "MAX_RETRIES":Settings.LLM_JUDGE_FOR_DATA_QUALITY_EVALUATION_MAX_RETRIES
        },
        "evalution":{
            "METRICS_EVALUATED_ON":Settings.DATA_QUALITY_EVALUATION_METRICS,
            "MIN_SCORE_POSSIBLE_PER_METRIC":Settings.DATA_QUALITY_EVALUATION_MIN_SCORE_POSSIBLE_PER_METRIC,
            "MAX_SCORE_POSSIBLE_PER_METRIC":Settings.DATA_QUALITY_EVALUATION_MAX_SCORE_POSSIBLE_PER_METRIC
        },
        "filtering":{
            "num_instances_before_filtering":num_instances_before_filtering,
            "num_instances_after_filtering":num_instances_after_filtering,
            "num_instances_filtered":num_instances_before_filtering-num_instances_after_filtering,
            "filtering_arguments":{
                "minimum_score_threshold":Settings.DATA_QUALITY_MINIMUM_SCORE_THRESHOLD
            }
        },
        "MEAN_SCORE_GIVEN_BY_LLM_AS_JUDGE":{
            "score":mean_evaluation_score_given_by_llm_as_judge
        }
    }

    return metadata