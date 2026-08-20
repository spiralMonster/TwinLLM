from pydantic import BaseModel
from fastapi import FastAPI,HTTPException

from application.model_generation_with_rag import call_llm_service_using_aws
from application.model_generation_with_rag import call_llm_service_using_gcp


app=FastAPI()


class QueryRequest(BaseModel):
    query:str


class QueryResponse(BaseModel):
    answer:str



@app.post("/generate_using_aws",response_model=QueryResponse)
async def generation_api_endpoint_for_aws(request:QueryRequest):
    try:
        prompt=request.query
        model_response=call_llm_service_using_aws(prompt=prompt)

        result={
            "answer":model_response
        }
        return result

    except Exception as e:
        raise HTTPException(status_code=500,detail=str(e)) from e



@app.post("/generate_using_gcp",response_model=QueryResponse)
async def generation_api_endpoint_for_gcp(request:QueryRequest):
    try:
        prompt=request.query
        model_response=call_llm_service_using_gcp(prompt=prompt)

        result={
            "answer":model_response
        }
        return result

    except Exception as e:
        raise HTTPException(status_code=500,detail=str(e)) from e