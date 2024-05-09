from transformers import AutoTokenizer
from TextGenerator import TextGenerator

import re

class JobChatBot():
    def __init__(self, text_generation_api_url, token):
        self.text_generator = TextGenerator(api_url=text_generation_api_url, token=token)
        self.tokenizer = AutoTokenizer.from_pretrained("meta-llama/Meta-Llama-3-8B-Instruct")
        
    def attachJob(self, job_dict):
        self.job = job_dict        
        self.job_requirements = self.job['requirements']
        
        tokens = self.tokenizer.tokenize(self.job_requirements)
        self.job_requirements_tokens = len(tokens)
        
    def attachCV(self, cv_dict):
        self.cv = cv_dict        
        self.cv_text = self.extractCVDictToText()
        
        tokens = self.tokenizer.tokenize(self.cv_text)
        self.cv_tokens = len(tokens)
        
    def extractCVDictToText(self):
        extract_keys=['Candidate\'s Profession',
                      'Candidate\'s Date of Birth',
                      'Candidate\'s Address',
                      'Candidate\'s Skills',
                      'Candidate\'s Experiences',
                      'Candidate\'s Education',
                      'Candidate\'s Certificates']
        extracted_cv_dict = {}
        
        for key in extract_keys:
            extracted_cv_dict[key] = self.cv[key]
                
        cv_text = ''
        for key, value in extracted_cv_dict.items():
            if value is None or '\n' not in value:
                cv_text = cv_text + key + ": " + str(value) + "\n"
            else:
                lines = value.split('\n')
                for i in range(len(lines)):
                    if '\t' not in lines[i]:
                        lines[i] = '\t' + lines[i]
                value = '\n'.join(lines)
                cv_text = cv_text + key + ":\n" + value + '\n'
        
        return cv_text
        
    def query(self, message):
        info_message = 'Candidate\'s CV:\n' + self.cv_text + '\n---\nJob Requirements:\n' + self.job_requirements
        request_message = info_message + '\n---\n' + message
        
        payload = {
            "inputs": request_message,
            "parameters": {
                "max_new_tokens": self.job_requirements_tokens + self.cv_tokens,
                "repetition_penalty": 1,
                "return_full_text": False
            }
        }
        
        response = self.text_generator.query(payload=payload)

        return response.strip()