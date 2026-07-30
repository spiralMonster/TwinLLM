from document_categories.vectordb_document_categories.chunked_documents.base.chunked_document import ChunkedDocument

def get_metadata(documents:list[ChunkedDocument]) -> dict:
    metadata={}

    for doc in documents:
        data_category=doc.get_category()
        author_name=doc.author_full_name

        if data_category not in metadata:
            metadata[data_category]=doc.metadata

        if "mean_chunk_size" not in metadata[data_category]:
            metadata[data_category]["mean_chunk_size"]=len(doc.content)

        else:
            metadata[data_category]["mean_chunk_size"]=(
                metadata[data_category]["mean_chunk_size"]+
                len(doc.content)
            )//2

        if "authors" not in metadata[data_category]:
            metadata[data_category]["authors"]=[]

        if author_name not in metadata[data_category]["authors"]:
            metadata[data_category]["authors"].append(author_name)

        metadata[data_category]["num_chunks"]=(
            metadata[data_category].get("num_chunks",0)+1
        )


    return metadata

