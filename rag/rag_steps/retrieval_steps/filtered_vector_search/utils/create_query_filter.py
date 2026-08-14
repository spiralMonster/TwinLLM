from qdrant_client.models import FieldCondition,Filter,MatchValue
from document_categories.rag_document_categories.query_document import Query


def create_filter(query:Query) -> Filter|None:
    author_full_name=query.author_full_name
    platform_name=query.platform

    if author_full_name:
        if platform_name:
            query_filter=Filter(
                must=[
                    FieldCondition(
                        key="author_full_name",
                        match=MatchValue(
                            value=author_full_name
                        )
                    ),
                    FieldCondition(
                        key="platform",
                        match=MatchValue(
                            value=platform_name
                        )
                    )
                ]
            )


        else:
            query_filter=Filter(
                must=[
                    FieldCondition(
                        key="author_full_name",
                        match=MatchValue(
                            value=author_full_name
                        )
                    )
                ]
            )


    else:
        if platform_name:
            query_filter=Filter(
                must=[
                    FieldCondition(
                        key="platform",
                        match=MatchValue(
                            value=platform_name
                        )
                    )
                ]
            )



        else:
            query_filter=None


    return query_filter