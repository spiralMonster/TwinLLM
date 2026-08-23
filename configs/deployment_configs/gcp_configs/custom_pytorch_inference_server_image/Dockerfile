FROM us-docker.pkg.dev/deeplearning-platform-release/gcr.io/huggingface-pytorch-inference-cu121.2-3.transformers.4-46.ubuntu2204.py311

ENV HF_HUB_ENABLE_HF_TRANSFER=1
ENV MODEL_ID=/opt/huggingface/model

RUN pip uninstall -y \
    torch \
    torchvision \
    torchaudio \
    transformers \
    tokenizers \
    safetensors


RUN pip install \
    --no-cache-dir \
    --retries 20 \
    --timeout 300 \
    --resume-retries 20 \
    "torch==2.8.0" \
    "transformers==5.14.1" \
    "tokenizers==0.22.2" \
    "safetensors==0.8.0"\
    google-cloud-storage


RUN pip install \
    --no-cache-dir \
    --retries 20 \
    --timeout 300 \
    --resume-retries 20 \
    "torchvision==0.23.0" \
    "torchaudio==2.8.0" \

RUN pip uninstall -y huggingface-inference-toolkit || true

RUN pip install --no-cache-dir fastapi

WORKDIR /app

COPY server.py /app/server.py

EXPOSE 8080

ENTRYPOINT ["uvicorn"]

CMD ["server:app","--host","0.0.0.0", "--port","8080"]




