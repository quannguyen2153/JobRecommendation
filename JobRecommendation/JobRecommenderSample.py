import pandas as pd
from CVParser import CVParser
from JobRecommender import JobRecommender

import time

API_URL = "https://api-inference.huggingface.co/models/meta-llama/Meta-Llama-3-8B-Instruct"
TOKEN = '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'

cv_parser = CVParser(text_generation_api_url=API_URL, token=TOKEN, cv_format_path='TextGeneration/cv_form.txt')

pdf_path = 'TextGeneration/sample_cv1.pdf'
cv_info = cv_parser.parseFromPDF(cv_pdf_path=pdf_path)

cv_dict = cv_parser.convertToDict(cv_info)



jobinfo_path='vietnamworks/data/vnw_jobinfo_full.json'
job_df = pd.read_json(jobinfo_path, encoding="utf-8")

job_recommender = JobRecommender()

start = time.time()

job_recommender.attachCV(cv_dict=cv_dict)
print(job_recommender.cv_text)

similarity_job_df = job_recommender.computeJobsSimilarity(job_df=job_df[:50])

similarity_job_df = similarity_job_df.sort_values(by='similarity', ascending=False)

print(similarity_job_df)
print(f'Completed in {time.time() - start}s')