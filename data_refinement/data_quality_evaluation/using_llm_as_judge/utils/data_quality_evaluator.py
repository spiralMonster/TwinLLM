from typing import Any
from loguru import logger

from langchain_core.prompts import ChatPromptTemplate
from langchain.chat_models import BaseChatModel
from langchain_mistralai import ChatMistralAI

from data_refinement.data_quality_evaluation.using_llm_as_judge.utils.data_quality_evaluator_specs import DataQualityEvaluatorSpecs

from utils.batch_data import batch
from utils.exceptions.model_exceptions.data_quality_evaluator_exception import DataQualityEvaluatorException

from settings import Settings


class DataQualityEvaluator:
    @staticmethod
    def initialize_llm_as_judge() -> BaseChatModel:
        model=ChatMistralAI(
            model_name=Settings.LLM_JUDGE_FOR_DATA_QUALITY_EVALUATION,
            api_key=Settings.LLM_JUDGE_FOR_DATA_QUALITY_EVALUATION_API_KEY,
            temperature=Settings.LLM_JUDGE_FOR_DATA_QUALITY_EVALUATION_TEMP,
            max_retries=Settings.LLM_JUDGE_FOR_DATA_QUALITY_EVALUATION_MAX_RETRIES
        )

        return model


    @staticmethod
    def generate_prompt() -> ChatPromptTemplate:
        template="""
        You are a Data Quality Evaluator.
        Your job is to evaluate the given Instruction-Output Pairs based on the following Metrics:
          - Helpfulness: Whether the content fully addresses the user's request and provides actionable guidance.
          - Correctness: Whether the content is factually accurate,logically sound and free of hallucinations.
          - Coherence: Whether the content is well organized,easy to follow, with ideas presented in logical sequence.
          - Complexity: Whether the content uses an appropriate level of depth and sophistication along with avoiding unnecessary complication.
          - Relevance: Whether the provided output is relevant to the instruction proposed.
          - Verbosity: Whether the content provides the right amount of details for the user's request.
        
        For each metric you have to output a score between 1 to 5.
        A score of '1' points to the worst and a score of '5' points to the best data quality.
        
        Instruction-Output Pairs:
        {instruction_output_pairs}
        """

        prompt=ChatPromptTemplate.from_template(
            template=template,
            input_variable=["instruction_output_pairs"]
        )

        return prompt


    @staticmethod
    def generate_evaluation_result(
            instruction_output_pairs:str,
            model:BaseChatModel,
            prompt:ChatPromptTemplate
    ) -> list[dict[str,Any]]:

        try:
            model=model.with_structured_output(
                DataQualityEvaluatorSpecs
            )

            chain=prompt|model
            response=chain.invoke(
                {
                    "instruction_output_pairs":instruction_output_pairs
                }
            )

            if not isinstance(response,DataQualityEvaluatorSpecs):
                logger.info("[Warning]: The model generated the invalid response!!!")
                return []

            else:
                results=[]
                for resp in response.evaluation_results:
                    result={
                        "helpfulness":resp.helpfulness,
                        "correctness":resp.correctness,
                        "coherence":resp.coherence,
                        "complexity":resp.complexity,
                        "relevance":resp.relevance,
                        "verbosity":resp.verbosity
                    }
                    results.append(result)

                return results

        except Exception as e:
            logger.info(f"Exception encountered: {e}")
            return []


    def evaluate(self,instruction_output_pairs:list[str],pair_per_prompt:int=3) -> list[dict[str,Any]]:
        model=self.initialize_llm_as_judge()
        prompt=self.generate_prompt()

        results=[]
        batch_instruction_output_pairs=batch(instruction_output_pairs,batch_size=pair_per_prompt)

        for pair_batch in batch_instruction_output_pairs:
            len_batch=len(pair_batch)

            evaluator_input="\n\n".join(pair_batch)
            evaluator_input=evaluator_input.strip("\n")

            evaluation_result=self.generate_evaluation_result(
                instruction_output_pairs=evaluator_input,
                model=model,
                prompt=prompt
            )

            if evaluation_result:
                results.extend(evaluation_result)

            else:
                result=[
                    {} for _ in range(len_batch)
                ]
                results.extend(result)


        if results:
            return results

        else:
            logger.info("Failed to evaluate data quality using LLM as judge.")
            raise DataQualityEvaluatorException("Failed to evaluate the data quality")







