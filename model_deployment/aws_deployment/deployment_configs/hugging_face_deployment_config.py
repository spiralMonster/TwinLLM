import json
from settings import Settings

hugging_face_deploy_config={
    "HF_MODEL_ID":Settings.DEPLOY_MODEL_ID,
    "HUGGING_FACE_HUB_TOKEN":Settings.HF_TOKEN,
    "SM_NUM_GPUS":json.dumps(Settings.SM_NUM_GPUS),
    "MAX_INPUT_LENGTH":json.dumps(Settings.MAX_INPUT_LENGTH),
    "MAX_TOTAL_TOKENS":json.dumps(Settings.MAX_TOTAL_TOKENS),
    "MAX_BATCH_TOTAL_TOKENS":json.dumps(Settings.MAX_BATCH_TOTAL_TOKENS),
    "MAX_BATCH_PREFILL_TOKENS":json.dumps(Settings.MAX_BATCH_TOTAL_TOKENS),
    "HF_MODEL_QUANTIZE":"bitsandbytes"

}