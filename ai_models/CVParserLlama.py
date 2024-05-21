from .CVParserModel import CVParserModel

from transformers import AutoTokenizer

import requests

class CVParserLlama(CVParserModel):
    def __init__(self, model_url, token, cv_format):
        # Tokenizer for calculating the number of tokens
        self.tokenizer = AutoTokenizer.from_pretrained(model_url, token=token)
        
        # Llama authentication
        self.api_url = 'https://api-inference.huggingface.co/models/' + model_url
        self.token = token        
        self.headers = {"Authorization": f"Bearer {self.token}"}
        
        self.cv_format = cv_format
        
        # Calculate the number of tokens of cv format in advance
        tokens = self.tokenizer.tokenize(self.cv_format)
        self.cv_format_tokens = len(tokens)
    
    def query(self, cv_text, threshold_tokens=1000):
        # Construct the extraction message
        cv_extraction_msg = '\"' + cv_text \
                            + '\"\n---\nExtract information from this CV into the following JSON format with utf-8 encoding:\n' \
                            + self.cv_format
                           
        # Calculate total tokens of input                    
        tokens = self.tokenizer.tokenize(cv_text)
        cv_tokens = len(tokens)
        total_tokens = cv_tokens + self.cv_format_tokens
              
        # Construct payload              
        cv_extraction_payload = {
            "inputs": cv_extraction_msg,
            "parameters": {
                "max_new_tokens": threshold_tokens if total_tokens < threshold_tokens else total_tokens,
                "return_full_text": False
            }
        }
        
        # Get response
        cv_extraction_output = requests.post(self.api_url, headers=self.headers, json=cv_extraction_payload)        
        cv_extraction_output = cv_extraction_output.json()[0]['generated_text'].strip()

        return cv_extraction_output