from .JobGPT import JobGPT

from .config import GPT_MODEL_NAME, GPT_TOKEN

class JobChatBot():
    def __init__(self, model):
        self.model = model
        
    def attachJob(self, job_dict, topic=None):
        self.job_dict = job_dict
        self.topic = topic
        
        # Change the model's job text to the selected topic        
        if self.topic is not None:
            self.job_text = self.extractTopicFromJobDict(job_dict=self.job_dict, topic=self.topic)
        else:                    
            self.job_text = self.extractJobDictToText(job_dict=self.job_dict)
        
        self.model.attachJob(job_text=self.job_text, topic=self.topic)
        
    def extractTopicFromJobDict(self, job_dict, topic):
        return job_dict[topic]
        
    def extractJobDictToText(self, job_dict):
        extract_keys = ['job_title',
                        'job_description',
                        'benefits',
                        'requirements']
        
        # Get necessary information
        extracted_job_dict = {}
        
        for key in extract_keys:
            extracted_job_dict[key] = job_dict[key]
        
        # Convert to text
        job_text = ''
        for key, value in extracted_job_dict.items():
            job_text = job_text + key + ":\n" + str(value) + '\n'
        
        return job_text
        
    def attachCV(self, cv_dict):
        self.cv_dict = cv_dict        
        self.cv_text = self.extractCVDictToText(cv_dict=self.cv_dict)
        
        self.model.attachCV(self.cv_text)
        
    def extractCVDictToText(self, cv_dict):
        extract_keys=['Profession',
                      'Skills',
                      'Experiences',
                      'Education',
                      'Certificates']
        
        # Get necessary information
        extracted_cv_dict = {}
        
        for key in extract_keys:
            extracted_cv_dict[key] = cv_dict[key]

        # Convert to text     
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
        response = self.model.query(message=message)
        return response.strip()

    @staticmethod
    def send_message(job_dict, cv_dict, message):
        try:
            jobgpt_model = JobGPT(model_name=GPT_MODEL_NAME, token=GPT_TOKEN)
            chat_bot = JobChatBot(model=jobgpt_model)
            chat_bot.attachJob(job_dict=job_dict, topic=None)
            chat_bot.attachCV(cv_dict=cv_dict)
            return chat_bot.query(message)
        except Exception as e:
            raise Exception('Chat error:' + str(e))