from loguru import logger

from document_categories.vectordb_document_categories.embedded_documents.base.embedded_document import EmbeddedDocument
from document_categories.rag_document_categories.query_document import Query

from rag.rag_steps.base.rag_step import RagStep

from rag.rag_steps.retrieval_steps.filtered_vector_search.search_over.dispatcher.filtered_vector_search_dispatcher import FilteredVectorSearchDispatcher
from rag.rag_steps.retrieval_steps.filtered_vector_search.utils.create_query_filter import create_filter


class FilteredVectorSearch(RagStep):
    def generate(self,query:Query,*args,**kwargs) -> list[EmbeddedDocument]:
        documents_to_retrieved=kwargs.get("documents_to_retrieved",5)

        query_content=query.content
        query_type=query.query_type

        if not query_type:
            query_type=["None"]

        query_filters=create_filter(query=query)

        retrieved_docs=[]
        dispatcher=FilteredVectorSearchDispatcher

        for doc_type in query_type:
            docs=dispatcher.dispatch(
                document_type=doc_type,
                query=query_content,
                documents_to_retrieved=documents_to_retrieved,
                filters=query_filters

            )

            retrieved_docs.extend(docs)


        retrieved_docs=set(retrieved_docs)
        retrieved_docs=list(retrieved_docs)

        logger.info("Filtered Vector Search completed successfully.")
        print(f"Number of documents retrieved: {len(retrieved_docs)}")

        return retrieved_docs




