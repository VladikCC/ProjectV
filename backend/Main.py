from fastapi import FastAPI
from pydantic import BaseModel
import psycopg2
import os
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

conn = psycopg2.connect(
    dbname=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    host=os.getenv("DB_HOST")
)
cursor = conn.cursor()

class Score(BaseModel):
    name: str
    score: int

@app.post("/score")
def add_score(score: Score):
    cursor.execute(
        "INSERT INTO scores (name, score) VALUES (%s, %s)",
        (score.name, score.score)
    )
    conn.commit()
    return {"status": "ok"}

@app.get("/scores")
def get_scores():
    cursor.execute("SELECT name, score FROM scores ORDER BY score DESC LIMIT 10")
    rows = cursor.fetchall()
    return rows