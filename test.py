import click


@click.command()
@click.option(
    "--run-etl",
    is_flag=True,
    default=False
)
@click.option(
"--run-rag-feature-pipeline",
    is_flag=True,
    default=False
)
def run(
        run_etl:bool=False,
        run_rag_feature_pipeline:bool=False
):
    if run_etl:
        print("Yes")

    elif run_rag_feature_pipeline:
        print("Rag")

    else:
        print("No")




if __name__=="__main__":
    run()
