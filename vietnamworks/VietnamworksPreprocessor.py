import pandas as pd
import csv

import re
import ast
import random
import time
from datetime import datetime, timedelta

from googletrans import Translator

class VNWPreprocessor():
    def __init__(self) -> None:
        self.translator = Translator()
        
    def convertToJSON(self, csv_input_path, json_output_path):
        df = pd.read_csv(csv_input_path)
        df.to_json(json_output_path, orient="records", indent=4, force_ascii=False)
        
    def saveDataframeToJSON(self, df, output_path):
        df.to_json(output_path, orient="records", indent=4, force_ascii=False)
        print('Wrote dataframe to {}.'.format(output_path))
        
    # Filter necessary fields
    def filterJobDataset(self, jobs_path, output_path=None):
        job_df = pd.read_json(jobs_path, encoding="utf-8")
        
        columns = ['job_title', 'job_url', 'company_name', 'company_url', 'location', 'post_date', 'due_date',
                        'fields', 'salary', 'experience', 'position', 'benefits', 'job_description', 'requirements']
        job_df = job_df[columns]
        
        if output_path is not None:
            self.saveDataframeToJSON(df=job_df, output_path=output_path)
        
        return job_df
            
    def standardizeJobDataset(self, jobs_path, output_path=None):
        job_df = pd.read_json(jobs_path, encoding="utf-8")        
        
        list_fields = ('location', 'fields', 'benefits')
        
        for field in list_fields:
            job_df[field] = job_df[field].apply(lambda x: ast.literal_eval(x))
            
        # Calculate due date and convert post_date to timestamp
        def extractRemainingTime(due_date_str):
            matches = re.findall(r'(\d+)\s+(tháng|ngày|giờ)', due_date_str)

            if matches:
                quantity, unit = matches[0]
                if unit == 'tháng':
                    months_remaining = int(quantity)
                    return months_remaining * 30
                if unit == 'ngày':
                    days_remaining = int(quantity)
                    return days_remaining
                elif unit == 'giờ':
                    hours_remaining = int(quantity)
                    return 0
            else:
                print("No number of months or days or hours found in the due_date string.")
                
        job_df['due_date'] = job_df['due_date'].apply(lambda x: \
            (datetime.now().replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(extractRemainingTime(x))).timestamp())
        
        job_df['post_date'] = job_df['post_date'].apply(lambda x: \
            datetime.strptime(x, "%d/%m/%Y").timestamp())
        
        # Convert empty experience values to null
        job_df['experience'] = job_df['experience'].apply(lambda x: x if x != 'Không hiển thị' else None)
            
        if output_path is not None:
            self.saveDataframeToJSON(df=job_df, output_path=output_path)
        
        return job_df
        
    def translateJobRequirements(self, jobs_path, output_path, job_idx=0):        
        df = pd.read_json(jobs_path, encoding="utf-8")
        
        if job_idx == 0:
            with open(output_path, 'a') as file:
                writer = csv.writer(file)
                writer.writerow(('job_title', 'company_name', 'requirements', 'requirements_language', 'en_requirements'))
        
        # Translate each job requirements
        for index, row in df.iloc[job_idx:].iterrows():
            job_title = row['job_title']
            company_name = row['company_name']
            job_req = row['requirements']
            
            print(row['job_url'])
            
            req_lang = self.translator.detect(job_req).lang
            
            if req_lang == 'en':
                en_req = ''
            else:
                en_req = self.translator.translate(job_req, src='auto', dest='en').text
                
            with open(output_path, 'a', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow((job_title, company_name, job_req, req_lang, en_req))
            
            print(f'Translated job {index}\'s requirements.')
            
            # Breaking time to avoid ban
            breaking_time = random.uniform(0.5, 1.5)
            print('Breaking time: {}...'.format(breaking_time))
            time.sleep(breaking_time)
            
    def addTranslationToJobInfo(self, jobs_path, translation_path, output_path=None):
        job_df = pd.read_json(jobs_path, encoding="utf-8")
        translation_df = pd.read_csv(translation_path, encoding="utf-8")

        # Add requirements_language and en_requirements to job_df DataFrame
        job_df['requirements_language'] = translation_df['requirements_language']
        job_df['en_requirements'] = translation_df['en_requirements']
        
        if output_path is not None:
            self.saveDataframeToJSON(df=job_df, output_path=output_path)
            
        return job_df
        

        
if __name__ == '__main__':
    vnw_data_processor = VNWPreprocessor()
    
    src_path = 'vietnamworks/rawdata/jobinfotest.json'
    filter_path = 'vietnamworks/rawdata/filteredjobinfotest.json'
    standard_path = 'vietnamworks/rawdata/standardjobinfotest.json'
    translation_path = 'vietnamworks/rawdata/translation.csv'
    
    vnw_data_processor.filterJobDataset(jobs_path=src_path, output_path=filter_path)
    vnw_data_processor.standardizeJobDataset(jobs_path=filter_path, output_path=standard_path)
    vnw_data_processor.translateJobRequirements(jobs_path=standard_path, output_path=translation_path)
    vnw_data_processor.addTranslationToJobInfo(jobs_path=standard_path, translation_path=translation_path, output_path='vietnamworks/rawdata/final.json')