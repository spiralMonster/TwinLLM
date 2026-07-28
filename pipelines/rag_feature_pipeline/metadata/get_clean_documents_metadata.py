from document_categories.vectordb_document_categories.cleaned_documents.base.cleaned_document import CleanedDocument

MAX_CONTENT_LENGTH=10000
MIN_CONTENT_LENGTH=0


def get_metadata(documents:list[CleanedDocument]) -> dict:
    metadata=dict()
    metadata["total_num_documents"]=len(documents)

    for doc in documents:
        data_category=doc.get_category()
        author_full_name=doc.author_full_name

        content_length=len(doc.content.split(" "))

        if data_category not in metadata:
            metadata[data_category]={}

        if "authors" not in metadata[data_category]:
            metadata[data_category]["authors"]=[]

        if author_full_name not in metadata[data_category]["authors"]:
            metadata[data_category]["authors"].append(author_full_name)


        if "mean_content_length" not in metadata[data_category]:
            metadata[data_category]["mean_content_length"]=content_length

        else:
            metadata[data_category]["mean_content_length"]=(
                metadata[data_category]["mean_content_length"]+
                content_length
            )//2

        metadata[data_category]["min_content_length"]=min(
            metadata[data_category].get("min_content_length",MAX_CONTENT_LENGTH),
            content_length
        )

        metadata[data_category]["max_content_length"]=max(
            metadata[data_category].get("max_content_length",MIN_CONTENT_LENGTH),
            content_length

        )

        metadata[data_category]["num_documents"]=(
            metadata[data_category].get("num_documents",0)+1
        )




    for key,value in metadata.items():
        if isinstance(value,dict):
            for k,v in value.items():
                if isinstance(v,int):
                    if k!="num_documents":
                        metadata[key][k]=str(v)+" "+"tokens"


    return metadata
