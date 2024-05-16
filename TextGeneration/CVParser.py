import PyPDF2
import re
import json
import copy

from transformers import AutoTokenizer
from TextGenerator import TextGenerator

class CVParser():
    def __init__(self, text_generation_api_url, token, cv_format_path):
        self.tokenizer = AutoTokenizer.from_pretrained("meta-llama/Meta-Llama-3-8B-Instruct")
        self.text_generator = TextGenerator(api_url=text_generation_api_url, token=token)
        
        self.cv_format = self.readCVFormat(cv_format_path)        
        tokens = self.tokenizer.tokenize(self.cv_format)
        self.cv_format_tokens = len(tokens)
        
    def readCVFormat(self, cv_format_path):
        with open(cv_format_path, 'r') as file:
            cv_format = file.read()
        return cv_format
        
    def extractInformation(self, cv_raw_text, threshold_tokens=1000):
        cv_extraction_msg = '\"' + cv_raw_text \
                            + '\"\n---\nExtract information from this CV into the following JSON format with utf-8 encoding:\n' \
                            + self.cv_format
                            
        tokens = self.tokenizer.tokenize(cv_raw_text)
        cv_tokens = len(tokens)
        total_tokens = cv_tokens + self.cv_format_tokens
                            
        cv_extraction_payload = {
            "inputs": cv_extraction_msg,
            "parameters": {
                "max_new_tokens": threshold_tokens if total_tokens < threshold_tokens else total_tokens,
                "return_full_text": False
            }
        }
        
        cv_extraction_output = self.text_generator.query(payload=cv_extraction_payload)

        return cv_extraction_output
    
    def extractJSONFromText(self, text):
        json_pattern = r'\{.*\}'
        
        match = re.search(json_pattern, text, re.DOTALL)

        if match:
            json_str = match.group(0)
            json_data = json.loads(json_str)
            return json_data
        else:
            return None
    
    def standardizeCVDict(self, cv_dict, remove_duplicates=True):
        standardized_cv_dict = copy.deepcopy(cv_dict)
        
        def dictToText(dict_data):
            text = '. '.join(f"{key}: {'; '.join(value) if isinstance(value, list) else value}" for key, value in dict_data.items())            
            return text
                
        def removeDuplicates(list_data):
            unique_list = []
            existed_items = set()

            for item in list_data:
                if item not in existed_items:
                    unique_list.append(item)
                    existed_items.add(item)
            
            return unique_list
        
        for key in standardized_cv_dict:
            if isinstance(standardized_cv_dict[key], list):
                for i in range(len(standardized_cv_dict[key])):
                    if isinstance(standardized_cv_dict[key][i], dict):
                        standardized_cv_dict[key][i] = dictToText(standardized_cv_dict[key][i])
                        
                if remove_duplicates:
                    standardized_cv_dict[key] = removeDuplicates(list_data=standardized_cv_dict[key])
                    
            elif isinstance(standardized_cv_dict[key], dict):
                standardized_cv_dict[key] = dictToText(standardized_cv_dict[key])
                
        return standardized_cv_dict
    
    def parseFromPDF(self, cv_pdf_path, extract_json=True, threshold_tokens=1000):
        pages = []
        with open(cv_pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)

            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                pages.append(page.extract_text())

        cv_raw_text = '\n'.join(pages)

        cv_info = self.extractInformation(cv_raw_text=cv_raw_text, threshold_tokens=threshold_tokens)
        
        if extract_json:
            cv_info = self.extractJSONFromText(text=cv_info)
        
        return cv_info