from document_categories.vectordb_document_categories.chunked_documents.base.chunked_document import ChunkedDocument


def get_metadata(documents:list[ChunkedDocument]) -> dict:
    metadata=dict()
    metadata["total_chunks"]=len(documents)

    for doc in documents:
        data_category=doc.get_category()
        author_name=doc.author_full_name

        if data_category not in metadata:
            metadata[data_category]={}

        metadata[data_category]["num_chunks"]=(
            metadata[data_category].get("num_chunks",0)+1
        )

        if "authors" not in metadata[data_category]:
            metadata[data_category]["authors"]=[]

        if author_name not in metadata[data_category]["authors"]:
            metadata[data_category]["authors"].append(author_name)


    return metadata


