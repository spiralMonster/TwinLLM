from document_categories.nosql_db_document_categories.base.base_document import Document


def get_metadata(documents:list[Document]) -> dict:
    metadata=dict()
    metadata["total_num_documents"]=len(documents)

    for doc in documents:
        collection=doc.get_collection_name()
        author_full_name=doc.author_full_name

        if collection not in metadata:
            metadata[collection]={}

        if "authors" not in metadata[collection]:
            metadata[collection]["authors"]=[]

        if author_full_name not in metadata[collection]["authors"]:
            metadata[collection]["authors"].append(author_full_name)

        metadata[collection]["num_documents"]=metadata[collection].get("num_documents",0)+1


    return metadata





