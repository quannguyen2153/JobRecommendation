from JobChatBotModel import JobChatBotModel

from transformers import AutoTokenizer
from TextGenerator import TextGenerator

class JobLlama(JobChatBotModel):
    def __init__(self, model_url, token):
        # Tokenizer for calculating the number of tokens
        self.tokenizer = AutoTokenizer.from_pretrained(model_url, token=token)
        
        # Text Generator for querying
        api_url = 'https://api-inference.huggingface.co/models/' + model_url        
        self.text_generator = TextGenerator(api_url=api_url, token=token)
        
    def selectTopic(self, topic):
        self.topic = topic
    
    def attachJob(self, job_text):
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
        response = self.text_generator.query(payload=payload)

        return response.strip()