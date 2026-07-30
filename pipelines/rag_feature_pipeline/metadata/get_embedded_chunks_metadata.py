from document_categories.vectordb_document_categories.embedded_documents.base.embedded_document import EmbeddedDocument


def get_metadata(documents:list[EmbeddedDocument]) -> dict:
    metadata={}

    for doc in documents:
        data_category=doc.get_category()
        author_name=doc.author_full_name

        if data_category not in metadata:
            metadata[data_category]=doc.metadata

        if "authors" not in metadata[data_category]:
            metadata[data_category]["authors"]=[]

        if author_name not in metadata[data_category]["authors"]:
            metadata[data_category]["authors"].append(author_name)

        metadata[data_category]["num_embedded_chunks"]=(
            metadata[data_category].get("num_embedded_chunks",0)+1
        )


    return metadata