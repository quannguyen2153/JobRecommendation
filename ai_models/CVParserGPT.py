from .CVParserModel import CVParserModel

from openai import OpenAI

class CVParserGPT(CVParserModel):
    def __init__(self, model_name, token, cv_format):
        self.model_name = model_name
        self.client = OpenAI(api_key=token)
        
        self.cv_format = cv_format
    
    def query(self, cv_text):
        # Construct the extraction message
        cv_extraction_msg = '\"' + cv_text \
                            + '\"\n---\nExtract information from this CV into the following JSON format with utf-8 encoding:\n' \
                            + self.cv_format
        
        # Query
        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=[
                {"role": "system", "content": "You are a CV extractor to extract CV information into a corresponding format."},
                {"role": "user", "content": cv_extraction_msg}
            ]
        )
        
        return response.choices[0].message.content