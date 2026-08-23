import os

import torch
from fastapi import FastAPI, HTTPException
from google.cloud import storage
from pydantic import BaseModel, Field
from transformers import AutoTokenizer, AutoModelForCausalLM


MODEL_PATH = os.getenv(
    "MODEL_ID",
    "/opt/huggingface/model",
)

AIP_STORAGE_URI = os.getenv("AIP_STORAGE_URI")

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
MODEL_DTYPE = (
    torch.bfloat16
    if DEVICE == "cuda"
    else torch.float32
)


app = FastAPI(
    title="Twin LLM Inference Server",
    version="1.0.0",
)


tokenizer = None
model = None


class GenerationParameters(BaseModel):

    max_new_tokens: int = Field(
        default=256,
        gt=0,
        le=4096,
    )

    do_sample: bool = True

    temperature: float = Field(
        default=0.7,
        gt=0.0,
        le=2.0,
    )

    top_p: float = Field(
        default=0.9,
        gt=0.0,
        le=1.0,
    )


class PredictionInstance(BaseModel):

    prompt: str = Field(
        min_length=1,
    )

    parameters: GenerationParameters = Field(
        default_factory=GenerationParameters
    )


class PredictionRequest(BaseModel):
    instances: list[PredictionInstance]




def download_model_artifacts():

    print("=" * 70)
    print("MODEL ARTIFACT INITIALIZATION")
    print("=" * 70)

    print(f"AIP_STORAGE_URI: {AIP_STORAGE_URI}")
    print(f"MODEL_PATH: {MODEL_PATH}")

    # --------------------------------------------------------
    # If the model already exists, don't download again.
    # --------------------------------------------------------

    if (
        os.path.isdir(MODEL_PATH)
        and os.listdir(MODEL_PATH)
    ):
        print(
            "Model artifacts already exist."
        )

        print(
            f"Skipping download from {AIP_STORAGE_URI}"
        )

        print("=" * 70)

        return


    if not AIP_STORAGE_URI:

        raise RuntimeError(
            "AIP_STORAGE_URI environment variable "
            "is not set."
        )

    if not AIP_STORAGE_URI.startswith("gs://"):

        raise RuntimeError(
            "Invalid AIP_STORAGE_URI: "
            f"{AIP_STORAGE_URI}"
        )



    gcs_path = AIP_STORAGE_URI[5:]
    bucket_name, _, prefix = gcs_path.partition("/")

    if not bucket_name:
        raise RuntimeError(
            f"Could not determine bucket from "
            f"AIP_STORAGE_URI: {AIP_STORAGE_URI}"
        )

    if prefix and not prefix.endswith("/"):
        prefix += "/"

    print(f"GCS bucket: {bucket_name}")
    print(f"GCS prefix: {prefix}")


    os.makedirs(
        MODEL_PATH,
        exist_ok=True,
    )

    client = storage.Client()
    bucket = client.bucket(bucket_name)

    print("Listing model artifacts...")

    blobs = bucket.list_blobs(
        prefix=prefix
    )

    downloaded_files = 0

    for blob in blobs:
        if blob.name.endswith("/"):
            continue

        if prefix:
            relative_path = blob.name[
                len(prefix):
            ]
        else:
            relative_path = blob.name

        if not relative_path:
            continue

        destination = os.path.join(
            MODEL_PATH,
            relative_path,
        )

        destination_directory = os.path.dirname(
            destination
        )

        os.makedirs(
            destination_directory,
            exist_ok=True,
        )

        print(
            f"Downloading:\n"
            f"  GCS: {blob.name}\n"
            f"  Local: {destination}"
        )

        blob.download_to_filename(
            destination
        )

        downloaded_files += 1


    if downloaded_files == 0:

        raise RuntimeError(
            "No model artifacts were downloaded "
            f"from {AIP_STORAGE_URI}"
        )

    print("=" * 70)

    print(
        f"Downloaded {downloaded_files} "
        "model artifact(s)."
    )

    print(
        f"Model artifacts available at: "
        f"{MODEL_PATH}"
    )

    print("=" * 70)



@app.on_event("startup")
def load_model():

    global tokenizer
    global model

    print("=" * 70)
    print("Twin LLM Inference Server")
    print("=" * 70)

    print(
        f"Model path: {MODEL_PATH}"
    )

    print(
        f"CUDA available: "
        f"{torch.cuda.is_available()}"
    )

    print(
        f"Selected device: {DEVICE}"
    )

    print(
        f"Selected dtype: {MODEL_DTYPE}"
    )

    if torch.cuda.is_available():

        print(
            f"GPU: "
            f"{torch.cuda.get_device_name(0)}"
        )

        print(
            f"CUDA version: "
            f"{torch.version.cuda}"
        )

    print("=" * 70)


    print("Initializing model artifacts...")

    download_model_artifacts()


    if not os.path.isdir(MODEL_PATH):

        raise RuntimeError(
            f"Model directory does not exist: "
            f"{MODEL_PATH}"
        )

    if not os.listdir(MODEL_PATH):

        raise RuntimeError(
            f"Model directory is empty: "
            f"{MODEL_PATH}"
        )

    print(
        f"Model directory verified: "
        f"{MODEL_PATH}"
    )

    print("=" * 70)

    print("Loading tokenizer...")

    tokenizer = AutoTokenizer.from_pretrained(
        MODEL_PATH,
        local_files_only=True,
        fix_mistral_regex=True,
    )

    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token

    print(
        "Tokenizer loaded successfully."
    )


    print("Loading model...")

    print(
        f"Using dtype: {MODEL_DTYPE}"
    )

    print(
        f"Using device: {DEVICE}"
    )

    model = AutoModelForCausalLM.from_pretrained(
        MODEL_PATH,
        dtype=MODEL_DTYPE,
        local_files_only=True,
    )


    model.to(DEVICE)

    model.eval()

    model_device = next(
        model.parameters()
    ).device


    print("=" * 70)
    print("MODEL LOADED SUCCESSFULLY")
    print("=" * 70)

    print(
        f"Model device: {model_device}"
    )

    print(
        f"Model dtype: "
        f"{next(model.parameters()).dtype}"
    )

    if torch.cuda.is_available():

        print(
            f"GPU memory allocated: "
            f"{torch.cuda.memory_allocated() / 1024**3:.2f} GB"
        )

        print(
            f"GPU memory reserved: "
            f"{torch.cuda.memory_reserved() / 1024**3:.2f} GB"
        )

    print("=" * 70)



@app.get("/health")
async def health():

    return {
        "status": "healthy"
    }



@app.post("/predict")
def predict(
    request: PredictionRequest
):

    if model is None or tokenizer is None:

        raise HTTPException(
            status_code=503,
            detail="Model is not loaded.",
        )

    predictions = []

    input_device = next(
        model.parameters()
    ).device

    # --------------------------------------------------------
    # Process each instance
    # --------------------------------------------------------

    for instance in request.instances:
        prompt = instance.prompt
        params = instance.parameters


        inputs = tokenizer(
            prompt,
            return_tensors="pt",
        )


        inputs = {
            key: value.to(input_device)
            for key, value in inputs.items()
        }


        generation_kwargs = {
            "max_new_tokens": params.max_new_tokens,
            "do_sample": params.do_sample,
            "pad_token_id": tokenizer.pad_token_id,
        }

        if params.do_sample:
            generation_kwargs.update(
                {
                    "temperature": params.temperature,
                    "top_p": params.top_p,
                }
            )

        with torch.inference_mode():
            outputs = model.generate(
                **inputs,
                **generation_kwargs,
            )


        generated_tokens = outputs[
            0,
            inputs["input_ids"].shape[-1]:
        ]

        generated_text = tokenizer.decode(
            generated_tokens,
            skip_special_tokens=True,
        )

        predictions.append(
            {
                "prediction": generated_text,
            }
        )


    return {
        "predictions": predictions,
    }