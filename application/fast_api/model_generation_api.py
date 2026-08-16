from pydantic import BaseModel
from fastapi import FastAPI,HTTPException

app=FastAPI()


class QueryRequest(BaseModel):
    query:str


class QueryResponse(BaseModel):
    answer:str



@app.post("/generate",response_model=QueryResponse)
async def generation_api_endpoint(request:QueryRequest):
    try:
        model_response=request.query+"This is the model response.."

        result={
            "answer":model_response
        }
        return result

    except Exception as e:
        raise HTTPException(status_code=500,detail=str(e)) from e