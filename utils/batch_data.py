from typing import Any

def batch(data:list[Any],batch_size:int) -> list[list[Any]]:
    batches=[]

    len_data=len(data)
    num_batches=len_data//batch_size

    start_ind=0
    end_ind=batch_size
    for _ in range(num_batches):
        b=data[start_ind:end_ind]
        batches.append(b)

        start_ind+=batch_size
        end_ind+=batch_size

    final_batch=data[start_ind:]
    if final_batch:
        batches.append(final_batch)


    return batches
