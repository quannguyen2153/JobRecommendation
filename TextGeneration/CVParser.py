import PyPDF2
import re
from TextGenerator import TextGenerator

class CVParser():
    def __init__(self, text_generation_api_url, token, cv_format_path):
        self.text_generator = TextGenerator(api_url=text_generation_api_url, token=token)
        self.cv_format = self.getCVFormat(cv_format_path)
        self.cv_fields = self.getCVFields(cv_format_path)
        
    def getCVFormat(self, cv_format_path):
        with open(cv_format_path, 'r') as file:
            cv_format = file.read()
        return cv_format
            
    def getCVFields(self, cv_format_path):
        fields = []
        pattern = r'[^\w\']+'
        
        with open(cv_format_path, 'r') as file:
            line = file.readline()
            
            while line:
                fields.append((re.sub(pattern, ' ', line)).strip())
                line = file.readline()
                
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
    
    def parseFromPDF(self, cv_pdf_path, clean=True, max_new_tokens=1000):
        pages = []
        with open(cv_pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)

            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                pages.append(page.extract_text())

        cv_raw_text = '\n'.join(pages)

        cv_info_text = self.extractInformation(cv_raw_text=cv_raw_text, max_new_tokens=max_new_tokens)
        
        if clean:
            cv_info_text = self.cleanText(text=cv_info_text)
        
        return cv_info_text