FROM us-docker.pkg.dev/deeplearning-platform-release/gcr.io/huggingface-pytorch-inference-cu121.2-3.transformers.4-46.ubuntu2204.py311

# Remove incompatible preinstalled versions
RUN pip uninstall -y \
    torch \
    torchvision \
    transformers \
    tokenizers \
    safetensors

# Install the ML stack required by the model
RUN pip install \
    --no-cache-dir \
    --retries 20 \
    --timeout 300 \
    --resume-retries 20 \
    "torch==2.8.0" \
    "transformers==5.14.1" \
    "tokenizers==0.22.2" \
    "safetensors==0.8.0"

# Install torchvision compatible with torch 2.8.0
RUN pip install \
    --no-cache-dir \
    --retries 20 \
    --timeout 300 \
    --resume-retries 20 \
    "torchvision==0.23.0"