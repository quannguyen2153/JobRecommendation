from transformers import AutoTokenizer
from TextGenerator import TextGenerator

import re

class JobChatBot():
    def __init__(self, text_generation_api_url, token):
        self.text_generator = TextGenerator(api_url=text_generation_api_url, token=token)
        self.tokenizer = AutoTokenizer.from_pretrained("meta-llama/Meta-Llama-3-8B-Instruct")
        
    def attachJob(self, job_dict):
        self.job = job_dict
        
    def attachCV(self, cv_dict):
        self.cv = cv_dict
        extract_keys=['profession', 'address', 'skills', 'experiences', 'education', 'certificates']
        self.cv_text = self.extractCVDictToText(extract_keys=extract_keys)
        
    def extractCVDictToText(self, extract_keys):
        extracted_cv_dict = {}
        
        for cv_dict_key in self.cv.keys():
            if any(key.lower() in cv_dict_key.lower() for key in extract_keys):
                extracted_cv_dict[cv_dict_key] = self.cv[cv_dict_key]
                
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
        info_message = 'Candidate\'s CV:\n' + self.cv_text + '\n---\nJob Requirements:\n' + self.job
        request_message = info_message + '\n---\n' + message
        
        tokens = self.tokenizer.tokenize(request_message)
        num_tokens = len(tokens)
        
        payload = {
            "inputs": request_message,
            "parameters": {
                # "max_new_tokens": 1000,
                "return_full_text": False
            }
        }
        
        response = self.text_generator.query(payload=payload)

        return response