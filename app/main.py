from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from pathlib import Path
from .chatbot import CDPChatbot
import markdown
import uvicorn
import os

app = FastAPI()

# Ensure static directory exists
static_dir = Path("app/static")
static_dir.mkdir(parents=True, exist_ok=True)

# Mount static files
app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")

templates = Jinja2Templates(directory="app/templates")
chatbot = CDPChatbot()

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/ask")
async def ask_question(question: str = Form(...)):
    response = chatbot.answer_question(question)
    # Convert markdown to HTML
    response['answer'] = markdown.markdown(response['answer'])
    return response

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000) 