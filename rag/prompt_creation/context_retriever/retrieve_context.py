from document_categories.vectordb_document_categories.embedded_documents.base.embedded_document import EmbeddedDocument
from document_categories.rag_document_categories.query_document import Query

from rag.rag_steps.pre_retrieval_steps.self_querying import SelfQuerying
from rag.rag_steps.pre_retrieval_steps.query_reconstruction import QueryReconstruction
from rag.rag_steps.pre_retrieval_steps.query_expansion import QueryExpansion
from rag.rag_steps.pre_retrieval_steps.query_router import QueryRouter

from rag.rag_steps.retrieval_steps.filtered_vector_search.search import FilteredVectorSearch
from rag.rag_steps.post_retrieval_steps.reranker import Reranker

from settings import Settings


class ContextRetriever:
    def __init__(self):
        self.self_querying=SelfQuerying()
        self.query_reconstructor=QueryReconstruction()
        self.query_expander=QueryExpansion()
        self.query_router=QueryRouter()

        self.document_retriever=FilteredVectorSearch()
        self.document_reranker=Reranker()


    def retrieve(
            self,
            query:str,
    ) -> tuple[str,list[EmbeddedDocument]]:

        num_query_expansions=Settings.NUM_QUERY_EXPANSIONS
        docs_to_retrieve_per_query=Settings.DOCS_TO_RETRIEVE_PER_QUERY
        docs_to_keep_in_context=Settings.DOCS_TO_KEEP_IN_CONTEXT

        query=Query.from_str(content=query)

        query=self.self_querying.generate(query=query)
        query=self.query_reconstructor.generate(query=query)

        expanded_queries=self.query_expander.generate(
            query=query,
            expand_to=num_query_expansions
        )
        queries=[
            self.query_router.generate(query=q)
            for q in expanded_queries
        ]

        retrieved_documents=[]
        for query in queries:
            retrieved_document=self.document_retriever.generate(
                query=query,
                documents_to_retrieved=docs_to_retrieve_per_query
            )
            retrieved_documents.extend(retrieved_document)


        final_retrieved_documents=self.document_reranker.generate(
            query=query,
            retrieved_documents=retrieved_documents,
            keep_top_k=docs_to_keep_in_context
        )
        reconstructed_query=query.content

        return reconstructed_query,final_retrieved_documents