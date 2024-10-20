from fastapi import FastAPI
from pydantic import BaseModel
from rephraser import Rephraser
from enum import Enum

class SentenceLength(str,Enum):
    consise = "consise"
    elaborated = "elaborated"
    same = "same"

class Tone (str,Enum):
    neutral = "neutral"
    excited = "excited"
    calm = "calm"
    urgent = "urgent"
    professional = "professional"
    witty = "witty"
    authoritative = "authoritative"


class WholeTextRephraseInput(BaseModel):
    text: str
    sentence_length: SentenceLength
    tone: Tone

class SelectedTextRephraseInput(BaseModel):
    text: str
    selected_text: str
    sentence_length: SentenceLength
    tone: Tone


app = FastAPI()
rephraser= Rephraser()

@app.get("/")
def welcome():
    return {"text":"Welcome"}

@app.post("/whole-text")
def rephrase_whole_text(rephraseInput: WholeTextRephraseInput):
    text, sentence_length, tone  = rephraseInput.text, rephraseInput.sentence_length, rephraseInput.tone
    res = rephraser.rephrase_whole_text(text, sentence_length, tone)
    return res

@app.post("/selected-text")
def rephrase_selected_text(rephraseInput: SelectedTextRephraseInput):
    text, selected_text, sentence_length, tone = rephraseInput.text, rephraseInput.selected_text, rephraseInput.sentence_length, rephraseInput.tone
    res = rephraser.rephrase_selected_text(selected_text,text,sentence_length,tone)
    return res






