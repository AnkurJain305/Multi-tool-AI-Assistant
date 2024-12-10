import streamlit as st
import traceback
from app import summarize_video
import google.generativeai as genai
import os

# Configure GenAI API key for MedGPT 
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to get MedGPT response 
def get_gemini_response(question):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(question)
    return response.text

# Streamlit interface
def main():
    # Configure page settings
    st.set_page_config(page_title="Multi-tool AI Assistant", page_icon="🤖")

    # App title
    st.title("🤖 Multi-Tool AI Assistant")

    # Initialize session state
    if "summary" not in st.session_state:
        st.session_state.summary = None
    if "questions_and_answers" not in st.session_state:
        st.session_state.questions_and_answers = []
    if "youtube_url" not in st.session_state:
        st.session_state.youtube_url = ""
    if "summary_generated" not in st.session_state:
        st.session_state.summary_generated = False

    # Option to switch between functionalities (Video Summarization or MedGPT Q&A)
    app_mode = st.radio("Select App Mode", ("Video Summarization", "MedGPT"))

    if app_mode == "Video Summarization":
        # Video Summarization mode
        st.subheader("Enter Video URL for Summarization")

        # Input for YouTube URL
        st.session_state.youtube_url = st.text_input(
            "Enter Video URL", 
            st.session_state.youtube_url, 
            help="Paste the video URL here."
        )

        # Generate Summary
        if st.button("Generate Summary and Questions"):
            if st.session_state.youtube_url:
                try:
                    with st.spinner("Fetching and summarizing the video..."):
                        # Generate summary and questions
                        summary, questions_and_answers = summarize_video(st.session_state.youtube_url)
                        
                        # Save in session state
                        st.session_state.summary = summary
                        st.session_state.questions_and_answers = questions_and_answers
                        st.session_state.summary_generated = True
                    
                    st.success("Summary and questions generated successfully!")
                
                except Exception as e:
                    st.error(f"Error generating summary: {e}")
                    # Print full traceback to console
                    traceback.print_exc()
                    st.session_state.summary_generated = False
            else:
                st.warning("Please enter a valid URL.")

        # Display Summary if Available
        if st.session_state.summary:
            st.subheader("Video Summary")
            st.write(st.session_state.summary)

        # Display Questions and Answers
        if st.session_state.questions_and_answers:
            st.subheader("Generated Questions and Answers")
            
            # Ensure questions exist before trying to display
            for idx, qa in enumerate(st.session_state.questions_and_answers, 1):
                st.markdown(f"**{idx}. Question:** {qa.get('question', 'No question')}")
                st.markdown(f"**Answer:** {qa.get('answer', 'No answer')}")
                st.divider()

    elif app_mode == "MedGPT":
        # MedGPT Q&A mode
        st.subheader("Ask a Question to MedGPT")

        # Input for MedGPT Question
        question_input = st.text_input("Ask a question:")

        if st.button("Ask MedGPT"):
            if question_input:
                try:
                    with st.spinner("Fetching response from MedGPT..."):
                        # Get the response from MedGPT
                        response = get_gemini_response(question_input)
                        st.subheader("MedGPT's Response:")
                        st.write(response)
                
                except Exception as e:
                    st.error(f"Error generating response: {e}")
                    traceback.print_exc()
            else:
                st.warning("Please enter a question.")

if __name__ == "__main__":
    main()
