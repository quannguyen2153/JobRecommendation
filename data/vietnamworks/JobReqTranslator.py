import pandas as pd
import csv

from googletrans import Translator

import random
import time

class JobReqTranslator():
    def __init__(self) -> None:
        self.translator = Translator()
        
    def save(self, df, output_path):
        df.to_json(output_path, orient="records", indent=4, force_ascii=False)
        print('Wrote {} jobs to {}.'.format(df.shape[0], output_path))
        
    def translateJobRequirements(self, jobinfo_path, output_path, job_idx=0): # job_idx begins from 0
        df = pd.read_json(jobinfo_path, encoding="utf-8")
        
        if job_idx == 0:
            with open(output_path, 'a') as file:
                writer = csv.writer(file)
                writer.writerow(('job_title', 'company_name', 'requirements', 'requirements_language', 'en_requirements'))
        
        for index, row in df.iloc[job_idx:].iterrows():
            job_title = row['job_title']
            company_name = row['company_name']
            job_req = row['requirements']
            
            print('Job {}\'s url: {}'.format(index, row['job_url']))
            
            req_lang = self.translator.detect(job_req).lang
            
            if req_lang == 'en':
                en_req = ''
            else:
                en_req = self.translator.translate(job_req, src='auto', dest='en').text
                
            with open(output_path, 'a', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow((job_title, company_name, job_req, req_lang, en_req))
            
            print(f'Translated job {index}\'s requirements.')
            
            breaking_time = random.uniform(0.5, 1.5)
            print('Breaking time: {}...'.format(breaking_time))
            time.sleep(breaking_time)
            
    def addTranslationToJobInfo(self, jobinfo_path, translation_path, output_path):
        job_df = pd.read_json(jobinfo_path, encoding="utf-8")
        translation_df = pd.read_csv(translation_path, encoding="utf-8")

        # Add requirements_language and en_requirements to job_df DataFrame
        job_df['requirements_language'] = translation_df['requirements_language']
        job_df['en_requirements'] = translation_df['en_requirements']
        
        self.save(df=job_df, output_path=output_path)
        

        
if __name__ == '__main__':
    job_req_translator = JobReqTranslator()
    
    jobinfo_path = 'vietnamworks/data/sample_data.json'
    translated_jobinfo_path = 'translated_job_req.csv'
    final_jobinfo_path = 'translated_sample_data.json'
    
    job_req_translator.translateJobRequirements(jobinfo_path=jobinfo_path, output_path=translated_jobinfo_path, job_idx=0)
    
    job_req_translator.addTranslationToJobInfo(jobinfo_path=jobinfo_path, translation_path=translated_jobinfo_path, output_path=final_jobinfo_path)