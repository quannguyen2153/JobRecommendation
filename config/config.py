LLAMA_MODEL_URL = 'meta-llama/Meta-Llama-3-8B-Instruct'
LLAMA_TOKEN = ''
GPT_MODEL_NAME = 'gpt-3.5-turbo-0125'
GPT_TOKEN = ''

FIREBASE_CONFIG = {
  'apiKey': "",
  'authDomain': "",
  'databaseURL': "",
  'projectId': "",
  'storageBucket': "",
  'messagingSenderId': "",
  'appId': "",
  'measurementId': "",
  'serviceAccount': "config/firebase-credential.json",
}

CV_JSON_FORMAT = \
'''
{
    "Profession": "",
    "Name": "",
    "Date of Birth": "",
    "Phone": "",
    "Address": "",
    "Email": "",
    "Website": "",
    "Skills": [],
    "Experiences": [],
    "Education": [],
    "Certificates": [],
    "References": []
}
'''

JOB_PAGE_SIZE = 5