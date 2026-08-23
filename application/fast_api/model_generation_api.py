from pydantic import BaseModel
from fastapi import FastAPI,HTTPException

from application.model_generation_with_rag import generate_using_aws
from application.model_generation_with_rag import generate_using_gcp


app=FastAPI()


class QueryRequest(BaseModel):
    query:str


class QueryResponse(BaseModel):
    answer:str



@app.post("/generate_using_aws",response_model=QueryResponse)
def generation_api_endpoint_for_aws(request:QueryRequest):
    try:
        prompt=request.query
        model_response=generate_using_aws(query=prompt)

        result={
            "answer":model_response
        }
        return result

    except Exception as e:
        raise HTTPException(status_code=500,detail=str(e)) from e



@app.post("/generate_using_gcp",response_model=QueryResponse)
def generation_api_endpoint_for_gcp(request:QueryRequest):
    try:
        prompt=request.query
        model_response=generate_using_gcp(query=prompt)

        result={
            "answer":model_response
        }
        return result

    except Exception as e:
        raise HTTPException(status_code=500,detail=str(e)) from e