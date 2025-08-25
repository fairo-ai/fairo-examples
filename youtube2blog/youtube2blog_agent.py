from langchain.tools import tool
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from pytubefix import YouTube
import tempfile
import openai
from pytubefix.cli import on_progress
import os
from pydantic import BaseModel, Field

class InputSchema(BaseModel):
    input: str = Field(description="The youtube video URL or ID")
    language: str = Field(description="The output language (e.g en, pt)")

def youtube2blog():
    def download_audio(video_id: str) -> str:
        yt = YouTube(f"https://youtu.be/{video_id}", on_progress_callback=on_progress)
        ys = yt.streams.get_audio_only()
        tmp = tempfile.NamedTemporaryFile(suffix=".m4a", delete=False)
        tmp_path = tmp.name
        tmp.close()
        folder, filename = os.path.split(tmp_path)
        ys.download(output_path=folder, filename=filename)
        return tmp_path
    
    def whisper_transcribe(file_path: str) -> str:
        with open(file_path, "rb") as audio:
            transcription = openai.audio.transcriptions.create(
                model="whisper-1", 
                file=audio
            )
        return transcription
    
    @tool(description="Extract transcripts from youtube videos")
    def youtube_transcript_tool(video_id: str) -> str:
        audio_file = download_audio(video_id)
        return whisper_transcribe(audio_file)

    template = """
    You are YouTube2BlogGPT, an expert at turning YouTube transcripts into ready-to-publish blog posts.
    You always:
    - Extract key points, structure them into headings and subheadings.
    - Rewrite in clear, engaging, SEO-friendly prose.
    - Provide a short introduction and conclusion for each post.
    - If no transcription is available, just answer you can't finish your task.
    - If the user provide a full youtube video link, you should extract only the videoID to use the tool
    
    When given a YouTube video ID, fetch its transcript and output a complete blog post draft.
    
    Youtube Video:
    {input}
    
    Language:
    {language}
    
    Agent Scratchpad:
    {agent_scratchpad}
    
    Begin!
    
    """
    prompt = PromptTemplate(
        input_variables=["input", "language", "agent_scratchpad"],
        template=template,
    )
    agent = create_tool_calling_agent(
        llm=ChatOpenAI(model_name="gpt-4o-mini"),
        prompt=prompt,
        tools=[youtube_transcript_tool]
    )
    
    executor = AgentExecutor(
        name="Youtube2Blog",
        verbose=True,
        tools=[youtube_transcript_tool],
        agent=agent,
        max_iterations=4,
        input_schema=InputSchema
    )
    
    return executor