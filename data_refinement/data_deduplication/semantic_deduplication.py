import re
import string
from typing import Any
from datasets import Dataset
import hnswlib

from models.embedding_model import EmbeddingModel

embedding_model=EmbeddingModel()
embedding_dim=embedding_model.embedding_size


def normalize_text(text: str) -> str:
    text=re.sub(r"\n+", " ", text)
    text=re.sub(r"\s\s+", " ", text)

    punctuation_table=str.maketrans("", "", string.punctuation)
    digit_table=str.maketrans("", "", string.digits)

    normalized_text=""
    words_in_text=text.split()
    for word in words_in_text:
        word=word.translate(punctuation_table)
        word=word.translate(digit_table)

        if word.isalpha():
            word=word.lower()
            normalized_text+=word
            normalized_text+=" "

    normalized_text=normalized_text.strip()
    return normalized_text


def semantic_deduplication(
        dataset:Dataset,
        instruction_key:str,
        output_key:str,
        minimum_cosine_similarity_threshold:float
) -> tuple[Dataset,dict[str,Any]]:
    
    metadata=dict()
    
    print(25 * "-" + "START:SEMANTIC DEDUPLICATION" + 25 * "-")
    initial_num_instances=len(dataset)
    
    dataset = dataset.map(
        lambda example: {
            "instruction_output_pair": f"Instruction:\n{example[instruction_key]}\n\nOutput:\n{example[output_key]}"
        }
    )

    index=hnswlib.Index(
        space="cosine",
        dim=embedding_dim
    )
    index.init_index(
        max_elements=len(dataset),
        ef_construction=200,
        M=32
    )
    index.set_ef(100)
    
    keep_ids=[]
    documents=list(dataset["instruction_output_pair"])
    
    for idx,document in enumerate(documents):
        normalized_document=normalize_text(text=document)
        embedded_doc=embedding_model(normalized_document,to_list=False)
        embedded_doc=embedded_doc.reshape(1,-1).astype("float32")

        if index.get_current_count()==0:
            index.add_items(embedded_doc,[idx])
            keep_ids.append(idx)
            continue
        
        labels,distances=index.knn_query(
            embedded_doc,
            k=min(10,index.get_current_count())
        )
        duplicate=False
        
        for distance in distances[0]:
            similarity=1-distance
            if similarity>=minimum_cosine_similarity_threshold:
                duplicate=True
                break
                
        
        if not duplicate:
            index.add_items(
                embedded_doc,
                [idx]
            )
            keep_ids.append(idx)
    
    
    dataset=dataset.remove_columns(["instruction_output_pair"])
    dataset=dataset.select(keep_ids)
    
    final_num_instances=len(dataset)
    print(f"[INFO] Total number of instances before Semantic Deduplication: {initial_num_instances}")
    print( f"[INFO] Total number of instances after Semantic Deduplication: {final_num_instances}")

    metadata["num_instances_before_deduplication"]=initial_num_instances
    metadata["num_instances_after_deduplication"]=final_num_instances

    print(25 * "-" + "END:SEMANTIC DEDUPLICATION" + 25 * "-")
    return dataset,metadata
    
    
    
            