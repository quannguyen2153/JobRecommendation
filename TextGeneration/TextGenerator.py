import requests

class TextGenerator():
    def __init__(self, api_url, token):
        self.api_url = api_url
        self.token = token
        
        self.headers = {"Authorization": f"Bearer {self.token}"}
        
    def query(self, payload):
        # Payload details url: https://huggingface.co/docs/api-inference/detailed_parameters
        
        response = requests.post(self.api_url, headers=self.headers, json=payload)
        result = response.json()[0]['generated_text']
        
        return result