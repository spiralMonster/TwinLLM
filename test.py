
if __name__=="__main__":
    from document_categories.vectordb_document_categories.embedded_documents.base.embedded_document import EmbeddedDocument
    from document_categories.vectordb_document_categories.embedded_documents.embedded_post_document import EmbeddedPostDocument
    from document_categories.vectordb_document_categories.embedded_documents.embedded_tweet_document import EmbeddedTweetDocument

    doc1=EmbeddedPostDocument(
        content="abc"
    )
    doc2=EmbeddedTweetDocument(
        content="pqr"
    )

    docs=[doc1,doc2]

    grouped_docs=EmbeddedDocument.group_by_class(docs)
    for cls,d in grouped_docs.items():
        print(type(d[0]))