import PyPDF2
import re
import json
import copy
from io import BytesIO

import ai_models.config as config
from .CVParserGPT import CVParserGPT

class CVParser():
    def __init__(self, model):
        self.model = model
        
    def extractInformation(self, cv_raw_text):
        cv_extraction_output = self.model.query(cv_text=cv_raw_text)
        return cv_extraction_output
    
    def extractJSONFromText(self, text):
        # Define JSON pattern
        json_pattern = r'\{.*\}'
        
        # Search for JSON string in text
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
        
        # Standardize each field in the cv dictionary (key (str) and value (str or str list))
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
    
    def parseFromPDF(self, cv_pdf_data, extract_json=True):
        # Read raw text from PDF and merge multiple pages into a single string
        pages = []
        pdf_reader = PyPDF2.PdfReader(BytesIO(cv_pdf_data))

        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            pages.append(page.extract_text())

        cv_raw_text = '\n'.join(pages)

        # Extract cv info as a string
        cv_info = self.extractInformation(cv_raw_text=cv_raw_text)
        
        # Extract cv info as a dict
        if extract_json:
            cv_info = self.extractJSONFromText(text=cv_info)
        
        return cv_info
    
    @staticmethod
    def parse_cv(cv_pdf_data):
      try:
        parser_gpt_model = CVParserGPT(model_name=config.GPT_MODEL_NAME, token=config.GPT_TOKEN, cv_format=config.CV_JSON_FORMAT)
        parser = CVParser(model=parser_gpt_model)
        cv_info_dict = parser.parseFromPDF(cv_pdf_data)
        cv_info_dict = parser.standardizeCVDict(cv_info_dict)
        return cv_info_dict
      except Exception as e:
        raise Exception("Parsing error:" + str(e))       