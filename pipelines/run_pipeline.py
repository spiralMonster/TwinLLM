import os
import click
from loguru import logger

from datetime import datetime as dt
from pathlib import Path

from pipelines.data_etl_pipeline.create_data_etl_pipeline import run_data_etl_pipeline
from pipelines.rag_feature_pipeline.create_rag_feature_pipeline import run_rag_feature_pipeline as run_rag_feat_pipeline
from pipelines.instruction_dataset_generating_pipeline.create_instruction_dataset_generating_pipeline import instruct_dataset_generating_pipeline


root_dir=str(Path(__file__).resolve().parent.parent)
default_etl_config_filename="data_etl_user1.yaml"
default_rag_feature_pipeline_config_filename="author_names.yaml"
default_instruction_dataset_generation_pipeline_config_filename="author_names.yaml"


@click.command(
    help="""
    This is the main entry point for the pipeline execution.
    Run the ZenMl pipelines with various options.

    Examples:
    \b
    # Run the pipeline with default options
    python run_pipeline.py

    \b
    # Run the pipeline without cache
    python run_pipeline.py --no-cache

    \b
    # Run only the ETL pipeline
    python run_pipeline.py --only-etl
    """
)

@click.option(
    "--no-cache",
    is_flag=True,
    default=False,
    help="Disable cache for the pipeline run"

)

@click.option(
    "--run-etl",
    is_flag=True,
    default=False,
    help="Whether to run the ETL pipeline"
)

@click.option(
    "--etl-config-filename",
    default=default_etl_config_filename,
    help="Filename of the ETL config file."
)

@click.option(
    "--run-rag-feature-pipeline",
    is_flag=True,
    default=False,
    help="Whether to run Rag feature pipeline."
)

@click.option(
    "--rag-feature-pipeline-config-filename",
    default=default_rag_feature_pipeline_config_filename,
    help="Filename of the Rag Feature Engineering config file."
)

@click.option(
    "--run-generate-instruct-dataset-pipeline",
    is_flag=True,
    default=False,
    help="Whether to run Instruct Dataset Generation pipeline."
)

@click.option(
    "--instruct-dataset-pipeline-config-filename",
    default=default_instruction_dataset_generation_pipeline_config_filename,
    help="Filename of the Instruction Dataset Generation config file."
)

def run(
        no_cache:bool=False,
        run_etl:bool=False,
        run_rag_feature_pipeline:bool=False,
        run_generate_instruct_dataset_pipeline:bool=False,
        etl_config_filename:str=default_etl_config_filename,
        rag_feature_pipeline_config_filename:str=default_rag_feature_pipeline_config_filename,
        instruct_dataset_pipeline_config_filename:str=default_instruction_dataset_generation_pipeline_config_filename
) -> None:
    assert(
        run_etl or run_rag_feature_pipeline or run_generate_instruct_dataset_pipeline
    ),"Please specify an action to run."

    pipeline_args={
        "enable_cache":not no_cache
    }

    if run_etl:
        run_args={}
        config_path=os.path.join(root_dir,"configs/pipeline_configs/data_etl_pipeline_configs",etl_config_filename)
        pipeline_run_name=f"data_etl_run_{dt.now().strftime('%Y_%m_%d_%H_%M_%S')}"

        assert os.path.exists(config_path),f"Config file not found: {config_path}"

        pipeline_args["run_name"]=pipeline_run_name
        pipeline_args["config_path"]=config_path

        run_data_etl_pipeline.with_options(**pipeline_args)(**run_args)

    elif run_rag_feature_pipeline:
        run_args={}
        config_path=os.path.join(
            root_dir,
            "configs/pipeline_configs/rag_feature_engineering_pipeline_configs",
            rag_feature_pipeline_config_filename
        )
        pipeline_run_name=f"rag_feature_pipeline_run_{dt.now().strftime('%Y_%m_%d_%H_%M_%S')}"

        assert os.path.exists(config_path), f"Config file not found: {config_path}"

        pipeline_args["run_name"]=pipeline_run_name
        pipeline_args["config_path"]=config_path

        run_rag_feat_pipeline.with_options(**pipeline_args)(**run_args)

    elif run_generate_instruct_dataset_pipeline:
        run_args={}
        config_path=os.path.join(
            root_dir,
            "configs/pipeline_configs/instruction_dataset_generating_pipeline_configs",
            instruct_dataset_pipeline_config_filename
        )
        pipeline_run_name=f"generate_instruct_dataset_run_{dt.now().strftime('%Y_%m_%d_%H_%M_%S')}"

        pipeline_args["run_name"]=pipeline_run_name
        pipeline_args["config_path"]=config_path

        instruct_dataset_generating_pipeline.with_options(**pipeline_args)(**run_args)







if __name__=="__main__":
    run()





