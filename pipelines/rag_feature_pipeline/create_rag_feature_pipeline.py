from zenml import pipeline

from pipelines.rag_feature_pipeline.steps.query_data_warehouse import query_data_warehouse
from pipelines.rag_feature_pipeline.steps.clean_documents import clean_documents
from pipelines.rag_feature_pipeline.steps.chunk_and_embed import chunk_and_embed
from pipelines.rag_feature_pipeline.steps.load_to_vector_db import load_to_vector_db


@pipeline
def run_rag_feature_pipeline(author_full_names:list[str]) -> list[str]:
    raw_documents=query_data_warehouse(author_full_names=author_full_names)

    cleaned_documents=clean_documents(raw_documents=raw_documents)
    last_step1=load_to_vector_db(documents=cleaned_documents,document_type="cleaned")

    embedded_docs=chunk_and_embed(cleaned_documents=cleaned_documents)
    last_step2=load_to_vector_db(documents=embedded_docs,document_type="embedded")

    return [last_step1.invocation_id,last_step2.invocation_id]