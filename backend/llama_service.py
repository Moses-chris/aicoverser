# services/llama_service.py
import requests

class LlamaService:
    def __init__(self):
        self.api_url = "https://api.grok.ai/v1/chat/completions"  # Replace with actual Grok API endpoint
        self.api_key = "YOUR_GROK_API_KEY"  # Replace with your actual API key

    def generate_response(self, prompt):
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        data = {
            "model": "llama-3-grok",
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 150
        }
        response = requests.post(self.api_url, headers=headers, json=data)
        if response.status_code == 200:
            return response.json()['choices'][0]['message']['content']
        else:
            raise Exception(f"Error in LLaMA API: {response.text}")