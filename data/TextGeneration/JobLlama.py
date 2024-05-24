from JobChatBotModel import JobChatBotModel

from transformers import AutoTokenizer

import requests

class JobLlama(JobChatBotModel):
    def __init__(self, model_url, token):
        # Tokenizer for calculating the number of tokens
        self.tokenizer = AutoTokenizer.from_pretrained(model_url, token=token)
        
        # Llama authentication
        self.api_url = 'https://api-inference.huggingface.co/models/' + model_url
        self.token = token        
        self.headers = {"Authorization": f"Bearer {self.token}"}
    
    def attachJob(self, job_text, topic):
        self.topic = topic if topic is not None else 'Job\'s Information'
        self.job_text = job_text
        
        # Calculate the number of tokens of job text in advance
        tokens = self.tokenizer.tokenize(self.job_text)
        self.job_tokens = len(tokens)
    
    def attachCV(self, cv_text):
        self.cv_text = cv_text
        
        # Calculate the number of tokens of CV text in advance
        tokens = self.tokenizer.tokenize(self.cv_text)
        self.cv_tokens = len(tokens)
    
    def query(self, message):
        # Construct message
        info_message = 'Candidate\'s CV:\n' + self.cv_text + f'\n---\n{self.topic}:\n' + self.job_text
        request_message = info_message + '\n---\n' + message
        
        # Construct payload
        payload = {
            "inputs": request_message,
            "parameters": {
                "max_new_tokens": self.job_tokens + self.cv_tokens,
                "repetition_penalty": 1,
                "return_full_text": False
            }
        }
        
        # Get response message
        response = requests.post(self.api_url, headers=self.headers, json=payload)        
        response = response.json()[0]['generated_text'].strip()

        return response