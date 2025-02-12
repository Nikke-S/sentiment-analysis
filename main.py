from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from transformers import pipeline
import requests

# Initialize FastAPI app
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins (change to specific URL for security)
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods (POST, GET, OPTIONS, etc.)
    allow_headers=["*"],  # Allows all headers
)

# Load Hugging Face model for sentiment analysis
hf_pipeline = pipeline("sentiment-analysis", model="NikkeS/imdb-distilbert")

# Define Groq Cloud API settings
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
GROQ_API_KEY = "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"

# Request model
class SentimentRequest(BaseModel):
    text: str
    model: str  # "custom" (Hugging Face) or "llama" (Groq)

# Response model
class SentimentResponse(BaseModel):
    sentiment: str
    confidence: float


@app.post("/analyze/")
def analyze_sentiment(request: SentimentRequest):
    if request.model == "custom":
        # Use fine-tuned Hugging Face model
        result = hf_pipeline(request.text)[0]
        label_mapping = {"LABEL_1": "positive", "LABEL_0": "negative"}
        sentiment = label_mapping.get(result["label"], "unknown")
        confidence = round(result["score"], 2)

    elif request.model == "llama":
        # Use Groq Cloud API (Llama 3)
        headers = {"Authorization": f"Bearer {GROQ_API_KEY}",
                   "Content-Type": "application/json"}
        payload = {
            "model": "llama-3.3-70b-versatile",
            "messages": [
                {"role": "user", "content": (
                    f"Analyze the sentiment of this text: \"{request.text}\".\n"
                    "Respond in JSON format like this: {\"sentiment\": \"positive\", \"confidence\": 0.92}."
                    "Sentiment can only be positive/negative, nothing else"
                    "Analyze sentiment and add confidence score according to that"
                    "Give confidence score with two digits"
                )}
            ]
        }

        response = requests.post(GROQ_API_URL, headers=headers, json=payload)

        # Extract response safely
        try:
            response_json = response.json()
            response_data = eval(
                response_json["choices"][0]["message"]["content"])
            sentiment = response_data.get("sentiment", "unknown")
            confidence = round(float(response_data.get("confidence", 0.0)), 2)
        except Exception:
            sentiment, confidence = "error", 0.0  # Default values on failure

    else:
        raise HTTPException(status_code=400, detail="Invalid model selection")

    return SentimentResponse(sentiment=sentiment, confidence=confidence)
