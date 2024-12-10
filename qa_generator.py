import os
from dotenv import load_dotenv
import google.generativeai as genai
import re

# Load environment variables
load_dotenv()

# Configure GenAI API key
genai.configure(api_key=os.getenv("c"))

def generate_questions_and_answers(summary, num_questions=5):
    """
    Generate questions and answers based on the summary using Google GenAI.

    Args:
        summary (str): The summary text.
        num_questions (int): Number of questions to generate.

    Returns:
        list: A list of dictionaries containing questions and answers.
    """
    try:
        # Construct the prompt for Google GenAI
        full_prompt = f""" You are an expert question generator. Based on the following summary, 
        generate {num_questions} meaningful questions and their respective answers. 
        Format each as:
        Q: [Question]
        A: [Answer]

        Summary:
        {summary}
        """
        
        # Make the API call to GenAI
        model = genai.GenerativeModel(model_name="gemini-pro")
        response = model.generate_content(full_prompt)

        # Process the response
        questions_and_answers = []
        
        # Use regex to parse questions and answers
        qa_pattern = r'Q:\s*(.*?)\s*A:\s*(.*?)(?=\n\nQ:|$)'
        matches = re.findall(qa_pattern, response.text, re.DOTALL)

        for question, answer in matches:
            questions_and_answers.append({
                "question": question.strip(),
                "answer": answer.strip()
            })

        return questions_and_answers

    except Exception as e:
        print(f"Error in generate_questions_and_answers: {e}")
        return []