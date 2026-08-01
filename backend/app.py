from fastapi import FastAPI
from backend.agent import ask_agent

app = FastAPI(
    title="MetricMind API",
    description="AI-powered Semantic BI Engine",
    version="1.0"
)

@app.get("/")
def home():
    return {"message": "Welcome to MetricMind API"}

@app.get("/ask")
def ask(question: str):
    answer = ask_agent(question)
    return {"question": question, "answer": answer}