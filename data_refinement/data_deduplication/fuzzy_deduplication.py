import re
import string
from datasets import Dataset
from datasketch import MinHash,MinHashLSH


def normalize_text(text:str) -> str:
    text=re.sub(r"\n+"," ",text)
    text=re.sub(r"\s\s+"," ",text)
    
    punctuation_table=str.maketrans("","",string.punctuation)
    digit_table=str.maketrans("","",string.digits)
    
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


def compute_shingles_from_text(text:str,shingle_length:int) -> list[str]:
    shingles=[]
    words=text.split()
    
    for i in range(len(words)-shingle_length+1):
        shingle=words[i:i+shingle_length]
        shingle=" ".join(shingle)
        shingle=shingle.strip()
        shingles.append(shingle)
    
    return shingles


def compute_minhash(shingles:list[str],number_of_hashes:int) -> MinHash:
    min_hash=MinHash(
        num_perm=number_of_hashes
    )
    
    for shingle in shingles:
        min_hash.update(shingle.encode("utf8"))
    
    return min_hash



def min_hash_deduplication(
        dataset:Dataset,
        instruction_key:str,
        output_key:str,
        shingle_length:int,
        number_of_hashes_per_document:int,
        minimum_similarity_threshold:float
) ->Dataset:

    print(25 * "-" + "START:FUZZY DEDUPLICATION USING MIN-HASH" + 25 * "-")
    initial_num_instances=len(dataset)
    
    dataset=dataset.map(
        lambda example:{
            "instruction_output_pair":f"Instruction:\n{example[instruction_key]}\n\nOutput:\n{example[output_key]}"
        }
    )
    
    lsh=MinHashLSH(
        threshold=minimum_similarity_threshold,
        num_perm=number_of_hashes_per_document
    )
    
    stored_minhash={}
    keep_docs=[]

    print("[INFO] Normalizing Text.")
    print("[INFO] Creating Shingles from Text.")
    print("[INFO] Computing MinHash of the Shingles.")
    print("[INFO] Creating LSH Index.")
    print("[INFO] Computing Jaccard Similarity between the documents in the same bucket.")
    print("[INFO] Removing similar documents.")

    documents=list(dataset["instruction_output_pair"])
    for idx,document in enumerate(documents):
        normalized_doc=normalize_text(text=document)
        doc_shingles=compute_shingles_from_text(text=normalized_doc,shingle_length=shingle_length)
        doc_min_hash=compute_minhash(shingles=doc_shingles,number_of_hashes=number_of_hashes_per_document)
        
        duplicate=False
        candidate_docs=lsh.query(doc_min_hash)
        
        for candidate_doc in candidate_docs:
            similarity=doc_min_hash.jaccard(
                stored_minhash[candidate_doc]
            )
            
            if similarity>=minimum_similarity_threshold:
                duplicate=True
                break
        
        if not duplicate:
            keep_docs.append(idx)
            lsh.insert(str(idx),doc_min_hash)
            stored_minhash[str(idx)]=doc_min_hash
    
    
    dataset=dataset.select(keep_docs)
    dataset=dataset.remove_columns(["instruction_output_pair"])
    
    print(f"[INFO] Total number of instances before Fuzzy deduplication using MIN-HASH Algorithm: {initial_num_instances}")
    print(f"[INFO] Total number of instances after Fuzzy deduplication using MIN-HASH Algorithm: {len(dataset)}")

    print(25 * "-" + "END:FUZZY DEDUPLICATION USING MIN-HASH" + 25 * "-")
    return dataset

