import PyPDF2
import re
from io import BytesIO

import ai_models.config as config
from ai_models.TextGenerator import TextGenerator

class CVParser():
    def __init__(self, text_generation_api_url, token, cv_format):
        self.text_generator = TextGenerator(api_url=text_generation_api_url, token=token)
        self.cv_format = cv_format
        self.cv_fields = self.getCVFields(cv_format)
            
    def getCVFields(self, cv_format):
        fields = []
        pattern = r'[^\w\']+'
    
        for line in cv_format.split('\n'):
            fields.append((re.sub(pattern, ' ', line)).strip())
                
        return fields
        
    def extractInformation(self, cv_raw_text, max_new_tokens=1000):
        cv_extraction_msg = '\"' + cv_raw_text \
                            + '\"\n---\nExtract information from this CV. Use the following sections:\n' \
                            + self.cv_format
                            
        cv_extraction_payload = {
            "inputs": cv_extraction_msg,
            "parameters": {
                "max_new_tokens": max_new_tokens,
                "return_full_text": False
            }
        }
        
        cv_extraction_output = self.text_generator.query(payload=cv_extraction_payload)

        return cv_extraction_output
    
    def cleanText(self, text):
        match = re.search(r'\w+\b', text[::-1])
        if match:
            last_word_index = len(text) - match.start()
            last_punctuation = text[last_word_index]
            return text[:last_word_index].rstrip(".,!?;:-\'\"") + last_punctuation
        else:
            return text.rstrip(".,!?;:-")
    
    def convertToDict(self, cv_info_text):
        cv_info_text = cv_info_text + '\n' + '* End.'
        
        cv_dict = dict.fromkeys(self.cv_fields)

        for field in self.cv_fields:
            match = re.search(fr"{re.escape(field)}:?(.*?)\n\*", cv_info_text, re.DOTALL)
            
            if match:
                cv_dict[field] = match.group(1).strip()

        return cv_dict
    
    def parseFromPDF(self, cv_pdf_data, clean=True, max_new_tokens=1000):
        pages = []
        pdf_reader = PyPDF2.PdfReader(BytesIO(cv_pdf_data))

        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            pages.append(page.extract_text())

        cv_raw_text = '\n'.join(pages)

        cv_info_text = self.extractInformation(cv_raw_text=cv_raw_text, max_new_tokens=max_new_tokens)

        if clean:
            cv_info_text = self.cleanText(text=cv_info_text)
        
        return cv_info_text
    
    @staticmethod
    def parse_cv(cv_pdf_data):
        parser = CVParser(config.API_URL, config.TOKEN, config.CV_FORM)
        cv_info_text = parser.parseFromPDF(cv_pdf_data)
        cv_info_dict = parser.convertToDict(cv_info_text)
        return cv_info_dict
        