from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import openai
import os
from typing import Dict

# Initialize FastAPI app
app = FastAPI(title="OpenAI Text Processing API")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Get OpenAI API key from environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")

class TextRequest(BaseModel):
    text: str

class TextResponse(BaseModel):
    response: str
    status: str

@app.post("/api/process")
async def process_text(request: TextRequest) -> Dict:
    try:
        # Call OpenAI API
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": request.text}
            ],
            max_tokens=150,
            temperature=0.7
        )
        
        return {
            "response": response.choices[0].message.content,
            "status": "success"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)