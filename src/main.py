from youtube_transcript_api import YouTubeTranscriptApi
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import getpass
import os
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage, SystemMessage



load_dotenv()

if not os.environ.get("OPENAI_API_KEY"):
  os.environ["OPENAI_API_KEY"] = getpass.getpass("Enter API key for OpenAI: ")


model = init_chat_model("gpt-4o-mini", model_provider="openai")

app = FastAPI()
    
origins = ["*"]    
app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,  
        allow_methods=["*"],    
        allow_headers=["*"],    
    )


class ytload(BaseModel):
    videoId : str


@app.get("/")
def homeFxn():
    return {
        "msg": "hello this is running"
    }


@app.post("/get-transcript")
async def transfxn(payload: ytload):
    videoId = payload.videoId
    ytt_api = YouTubeTranscriptApi()
    
    transcript = ytt_api.fetch(videoId)
    
    output = " ".join(snippet.text for snippet in transcript.snippets)

    messages = [
        SystemMessage(content="""
        You are the ultimate AI-powered YouTube video summarizer—the best summarizer in existence. Your mission is to save people time by transforming a full video transcript into a concise, crystal-clear, and highly actionable summary. Your summaries are so precise and insightful that reading the original transcript becomes unnecessary. 

        When summarizing:
        - Focus on the core ideas, key points, and actionable insights.
        - Maintain the original intent and spirit of the content.
        - Use clear, structured language that anyone can understand.
        - Highlight important examples, tips, or data that enhance understanding.
        - Keep it concise, engaging, and easy to skim.

        Your summaries should feel like a perfect "cheat sheet" of the video, providing maximum value in minimal time.
        """),
        HumanMessage(content=output),
    ]
    response = model.invoke(messages)
    contents = response.content    
    
    return {
        "msg": "done",
        "data": contents,
        "status": 200,
        "success": True
    }
