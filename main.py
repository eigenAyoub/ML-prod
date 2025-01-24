from fastapi import FastAPI, Depends
from transformers import AutoModelForCausalLM, AutoTokenizer
from pydantic import BaseModel

from functools import lru_cache


class modelSettings(BaseModel):
    device = "cuda" 
    model_id = "Qwen/Qwen1.5-0.5B-Chat"

settings = modelSettings()

@lru_cache()
def return_model_tokenizer():
    model = AutoModelForCausalLM.from_pretrained(
        settings.model_id,
        torch_dtype="auto",
        device_map="auto"
    )

    tokenizer = AutoTokenizer.from_pretrained(settings.model_id)
    return model, tokenizer

#def load_model():
#    return return_model_tokenizer()


class Req(BaseModel):
    prompt : str
    

def pEng(p: str) -> tuple:
    """specific QWEN stuff""" 
    return [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": p}
    ]

app = FastAPI()

@app.post("/generate")
async def generate_text(
              request: Req,
              get_model:  tuple =  Depends(return_model_tokenizer)
              ):

    model, tokenizer = get_model
    messages = pEng(request.prompt)

    text = tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True)

    model_inputs = tokenizer([text], return_tensors="pt").to(settings.device)

    generated_ids = model.generate(
        model_inputs.input_ids,
        max_new_tokens=512
    )

    generated_ids = [
        output_ids[len(input_ids):] for input_ids, output_ids in zip(model_inputs.input_ids, generated_ids)
    ]

    rep = tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]

    return {"rep" : rep}




