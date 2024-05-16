import pandas as pd
from CVParser import CVParser
from JobRecommender import JobRecommender

import time

API_URL = "https://api-inference.huggingface.co/models/meta-llama/Meta-Llama-3-8B-Instruct"
TOKEN = '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'

cv_parser = CVParser(text_generation_api_url=API_URL, token=TOKEN, cv_format_path='TextGeneration/cv_format.json')

pdf_path = 'TextGeneration/sample_cv3.pdf'
cv_dict = cv_parser.parseFromPDF(cv_pdf_path=pdf_path)

cv_dict = cv_parser.standardizeCVDict(cv_dict)



jobinfo_path='JobData/jobs.json'
job_df = pd.read_json(jobinfo_path, encoding="utf-8")

encoded_fields_path='JobRecommendation/encoded_fields.json'
field_df = pd.read_json(encoded_fields_path, encoding="utf-8")  

job_recommender = JobRecommender()

job_recommender.attachFields(field_df=field_df)
job_recommender.attachJobs(job_df=job_df)

start = time.time()

job_recommender.attachCV(cv_dict=cv_dict)
print(job_recommender.cv_text)

similarity_job_df = job_recommender.computeJobsSimilarity(sort=True, top_f=2)

print(similarity_job_df.head(50))
print(f'Completed in {time.time() - start}s')

print(similarity_job_df.head(50)['fields'])