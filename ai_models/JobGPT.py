from .JobChatBotModel import JobChatBotModel

from openai import OpenAI

class JobGPT(JobChatBotModel):
    def __init__(self, model_name, token):
        self.model_name = model_name
        self.client = OpenAI(api_key=token)
        
    def attachJob(self, job_text, topic):
        self.topic = topic if topic is not None else 'Job\'s Information'
        self.job_text = job_text
    
    def attachCV(self, cv_text):
        self.cv_text = cv_text
    
    def query(self, message):
        # Construct message
        info_message = 'My\'s CV:\n' + self.cv_text + f'\n---\n{self.topic}:\n' + self.job_text
        request_message = info_message + '\n---\n' + message + '\nAnswer in English.'
        
        # Query
        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=[
                {"role": "system", "content": "You are a job assistant to answer job related questions."},
                {"role": "user", "content": request_message}
            ]
        )
        
        return response.choices[0].message.content