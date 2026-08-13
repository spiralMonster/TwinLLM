from transformers import AutoTokenizer,AutoModelForCausalLM
from settings import Settings

if __name__=="__main__":
    model_id=Settings.PREFERENCE_MODEL

    tokenizer=AutoTokenizer.from_pretrained(
        model_id
    )

    model=AutoModelForCausalLM.from_pretrained(
        model_id,
        device_map="auto"
    )

    input_text="Write an article about supervised fine tuning."

    inputs=tokenizer([input_text],return_tensors="pt")

    output=model.generate(
        **inputs,
        max_seq_length=256
    )

    print(output)
