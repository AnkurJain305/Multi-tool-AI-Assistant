import os
from dotenv import load_dotenv
from youtube_transcript_api import YouTubeTranscriptApi
import google.generativeai as genai
from qa_generator import generate_questions_and_answers

# Load environment variables
load_dotenv()

# Configure GenAI API key
genai.configure(api_key=os.getenv("c"))

# Prompt for generating summary
summary_prompt = """You are a YouTube video summarizer. You will take the transcript text 
and summarize the video, providing the important points within 500 words. 
Please summarize the text given here: """

# Function to extract video ID from YouTube URL
def extract_video_id(url):
    try:
        if "v=" in url:
            video_id = url.split("v=")[1].split("&")[0]
        elif "youtu.be" in url:
            video_id = url.split("/")[-1]
        return video_id
    except IndexError:
        raise ValueError("Invalid YouTube URL.")

# Function to fetch transcript from YouTube
def extract_transcript_details(video_id):
    try:
        transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
        transcript = " ".join(item["text"] for item in transcript_list)
        return transcript
    except Exception as e:
        raise RuntimeError(f"Error fetching transcript: {e}")

# Function to generate summary using Google GenAI
def generate_summary(transcript_text):
    try:
        model = genai.GenerativeModel(model_name="gemini-pro")
        response = model.generate_content(summary_prompt + transcript_text)
        return response.text
    except Exception as e:
        raise RuntimeError(f"Error generating summary: {e}")

# Function to summarize a YouTube video and generate questions
def summarize_video(youtube_url):
    try:
        # Extract video ID
        video_id = extract_video_id(youtube_url)
        if not video_id:
            raise ValueError("Invalid YouTube URL.")

        # Fetch transcript
        transcript = extract_transcript_details(video_id)

        # Generate summary
        summary = generate_summary(transcript)

        # Generate questions and answers
        questions_and_answers = generate_questions_and_answers(summary)

        return summary, questions_and_answers
    except Exception as e:
        print(f"Error in summarize_video: {e}")
        raise