import os
import click
from loguru import logger

from datetime import datetime as dt
from pathlib import Path

from pipelines.data_etl_pipeline.create_data_etl_pipeline import run_data_etl_pipeline

root_dir=str(Path(__file__).resolve().parent.parent)
default_etl_config_filename="data_etl_user1.yaml"


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

def run(
        no_cache:bool=False,
        run_etl:bool=False,
        etl_config_filename:str=default_etl_config_filename
) -> None:
    assert(
        run_etl
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





if __name__=="__main__":
    run()





