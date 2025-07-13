import os
import google.generativeai as genai
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

# This line loads the API_KEY from your .env file
load_dotenv()

# --- 1. Basic Server Setup ---
app = Flask(__name__)
# CORS allows your future webpage to communicate with this server
CORS(app)

# --- 2. Configure the Google AI API ---
# It fetches the key you stored in the .env file
api_key = os.getenv("API_KEY")
if not api_key:
    # This is a safety check in case the key is missing
    raise ValueError("API_KEY not found. Please set it in the .env file.")
genai.configure(api_key=api_key)
# We specify which AI model we want to use
model = genai.GenerativeModel('gemini-1.5-flash-latest')

# --- 3. The AI Prompt "Brain" ---
# ** ACTION REQUIRED: Paste your perfected prompt from Phase 1 here **
PROMPT_TEMPLATE = """
You are an expert IELTS examiner with 15 years of experience. Your task is to analyze the following IELTS Writing Task 2 essay.

Provide a detailed, constructive, and encouraging analysis based on the four official IELTS band descriptors.

First, provide an estimated overall band score.

Then, for each of the four criteria, do the following:
1. Assign a band score for that specific criterion.
2. Provide a 2-3 sentence explanation for why you gave that score.
3. Give 2 specific, actionable bullet points for improvement.

The four criteria are:
- Task Achievement (TA)
- Coherence and Cohesion (CC)
- Lexical Resource (LR)
- Grammatical Range and Accuracy (GRA)

Format your entire response in Markdown. Use headings for each section.

Here is the essay to analyze:
---
{essay_text}
---
"""

# --- 4. The API "Endpoint" or the "Door" ---
# This creates a URL that our webpage can send the essay to
@app.route('/api/check-essay', methods=['POST'])
def check_essay():
    try:
        # Get the essay text sent from the webpage
        data = request.get_json()
        if not data or 'essay' not in data:
            return jsonify({'error': 'No essay text provided'}), 400

        user_essay = data['essay']
        
        # Insert the user's essay into our main prompt
        full_prompt = PROMPT_TEMPLATE.format(essay_text=user_essay)

        # Send the complete prompt to the Gemini API
        response = model.generate_content(full_prompt)
        
        # Send the AI's feedback text back to the webpage
        return jsonify({'feedback': response.text})

    except Exception as e:
        # If anything goes wrong, send back an error message
        print(f"An error occurred: {e}")
        return jsonify({'error': 'Failed to process the essay'}), 500

# --- 5. Code to Run the Server ---
if __name__ == '__main__':
    # This makes the server start listening for requests when we run the file
    app.run(debug=True, port=5000)