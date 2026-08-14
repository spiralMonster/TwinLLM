from qdrant_client.models import Filter
from document_categories.vectordb_document_categories.embedded_documents.base.embedded_document import EmbeddedDocument

from rag.rag_steps.retrieval_steps.filtered_vector_search.search_over.articles import filtered_vector_search_over_articles
from rag.rag_steps.retrieval_steps.filtered_vector_search.search_over.posts import filtered_vector_search_over_posts
from rag.rag_steps.retrieval_steps.filtered_vector_search.search_over.tweets import filtered_vector_search_over_tweets
from rag.rag_steps.retrieval_steps.filtered_vector_search.search_over.repositories import filtered_vector_search_over_repositories



class FilteredVectorSearchDispatcher:
    @classmethod
    def dispatch(
            cls,
            document_type:str,
            query:str,
            documents_to_retrieved:int,
            filters:Filter|None
    ) -> list[EmbeddedDocument]:
        
        if document_type=="Article":
            retrieved_documents=filtered_vector_search_over_articles(
                query=query,
                documents_to_retrieved=documents_to_retrieved,
                filters=filters
            )
        
        elif document_type=="Post":
            retrieved_documents=filtered_vector_search_over_posts(
                query=query,
                documents_to_retrieved=documents_to_retrieved,
                filters=filters
            )
        
        elif document_type=="Tweet":
            retrieved_documents=filtered_vector_search_over_tweets(
                query=query,
                documents_to_retrieved=documents_to_retrieved,
                filters=filters
            )
        
        elif document_type=="Code":
            retrieved_documents=filtered_vector_search_over_repositories(
                query=query,
                documents_to_retrieved=documents_to_retrieved,
                filters=filters
            )
            
        
        else:
            retrieved_documents=[]
            retrieved_documents.extend(
                filtered_vector_search_over_articles(
                    query=query,
                    documents_to_retrieved=documents_to_retrieved,
                    filters=filters,
                )  
            )
            retrieved_documents.extend(
                filtered_vector_search_over_posts(
                    query=query,
                    documents_to_retrieved=documents_to_retrieved,
                    filters=filters,
                )
            )
            retrieved_documents.extend(
                filtered_vector_search_over_tweets(
                    query=query,
                    documents_to_retrieved=documents_to_retrieved,
                    filters=filters,
                )
            )
            
            retrieved_documents.extend(
                filtered_vector_search_over_repositories(
                    query=query,
                    documents_to_retrieved=documents_to_retrieved,
                    filters=filters,
                )
            )


        return retrieved_documents
            