import os
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from llama_cpp import Llama
from huggingface_hub import hf_hub_download

app = FastAPI(title="Baher AI Backend")

MODEL_REPO = "Ishammari77/my-deepseek-model" 
MODEL_FILENAME = "model.gguf"

print("Downloading/Loading model from Hugging Face Hub...")

model_path = hf_hub_download(
    repo_id=MODEL_REPO, 
    filename=MODEL_FILENAME,
    token=os.environ.get("HF_TOKEN")
)

llm = Llama(
    model_path=model_path,
    n_ctx=2048,
    n_threads=4  
)

class ChatRequest(BaseModel):
    message: str

@app.get("/", response_class=HTMLResponse)
async def get_ui():
    with open("index.html", "r", encoding="utf-8") as f:
        return f.read()

@app.post("/chat")
async def chat_endpoint(request: ChatRequest):
    try:
        response = llm(
            f"### Instruction:\n{request.message}\n\n### Response:\n", 
            max_tokens=512, 
            stop=["### Instruction:"], 
            echo=False
        )
        return {"response": response['choices'][0]['text'].strip()}
    except Exception as e:
        return {"response": f"Error processing request: {str(e)}"}