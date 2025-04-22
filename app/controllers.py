from flask import request, jsonify, Blueprint, render_template
import requests
import json
import os
import markdown

controllers = Blueprint('controllers', __name__)

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

def call_openrouter_api(concept, audience):
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "<YOUR_SITE_URL>",  # Optional
        "X-Title": "<YOUR_SITE_NAME>"  # Optional
    }

    payload = {
        "model": "mistralai/mistral-small-3.1-24b-instruct:free",
        "messages": [
            {
                "role": "system",
                "content": "You are a creative assistant who explains complex concepts using metaphors or analogies. Avoid greetings or unnecessary phrases like 'sure' in your explanation."
            },
            {
                "role": "user",
                "content": f"Explain the concept '{concept}' to a {audience} using a metaphor or analogy."
            }
        ]
    }

    response = requests.post(url, headers=headers, data=json.dumps(payload))

    if response.status_code == 200:
        return response.json()  # Return the JSON response from OpenRouter API
    else:
        return f"Error: {response.status_code}, {response.text}"


def generate_metaphor():
    if request.method == 'POST':

        data = request.form

        concept = data.get("concept", "").strip() 
        audience = data.get("level", "").strip() 

        if not concept or not audience:
            return jsonify({"error": "Missing required fields: concept and knowledge_level"}), 400
        
        try:
        # Call the OpenRouter API
            metaphor_response = call_openrouter_api(concept, audience)
            metaphor_html = markdown.markdown(metaphor_response.get("choices", [{}])[0].get("message", {}).get("content", ""))

            return render_template('explain.html', output=metaphor_html)

        except Exception as e:
            return render_template('explian.html', error=str(e))
        
    return render_template('explain.html')

