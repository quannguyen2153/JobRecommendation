import PyPDF2
import re
import json
import copy

class CVParser():
    def __init__(self, model):
        self.model = model
        
    def extractInformation(self, cv_raw_text):
        cv_extraction_output = self.model.query(cv_text=cv_raw_text)
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
    
    def parseFromPDF(self, cv_pdf_path, extract_json=True):
        pages = []
        with open(cv_pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)

            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                pages.append(page.extract_text())

        cv_raw_text = '\n'.join(pages)

        cv_info = self.extractInformation(cv_raw_text=cv_raw_text)
        
        if extract_json:
            cv_info = self.extractJSONFromText(text=cv_info)
        
        return cv_info