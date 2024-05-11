import os
import pandas as pd
import json
import csv

from googletrans import Translator

import re
import random
import time
from datetime import datetime, timedelta

class VNWDataProcessor():
    def __init__(self) -> None:
        self.translator = Translator()
        
    def save(self, df, output_path):
        df.to_json(output_path, orient="records", indent=4, force_ascii=False)
        print('Wrote {} jobs to {}.'.format(df.shape[0], output_path))
        
    def mergeJobSegments(self, job_segments_dir, output_path, drop_duplicates=False):
        dfs = []
        for filename in os.listdir(job_segments_dir):
            if filename.endswith(".json"):
                file_path = os.path.join(job_segments_dir, filename)
                df = pd.read_json(file_path, encoding="utf-8")
                dfs.append(df)

        merged_df = pd.concat(dfs, ignore_index=True)
        
        if drop_duplicates:
            merged_df = merged_df.drop_duplicates()
        
        self.save(df=merged_df, output_path=output_path)
        
    def restructureJobInfo(self, jobinfo_path, output_path):
        df = pd.read_json(jobinfo_path, encoding="utf-8")
        
        # Rename columns
        name_map = {
            'title': 'job_title',
            'company': 'company_name',
            'end_date': 'due_date',
            'profession': 'fields',
            'pos_rank': 'position',
            'experienced_year': 'experience'
        }        
        df.rename(columns=name_map, inplace=True)
        
        # Drop unnecessary columns
        dropped_columns = ['field', 'skills', 'profile_language', 'nationality', 'tags']
        df.drop(columns=dropped_columns, inplace=True)
        
        # Reorder columns
        column_order = ['job_title', 'job_url', 'company_name', 'company_url', 'location', 'post_date', 'due_date',
                        'fields', 'salary', 'experience', 'position', 'benefits', 'job_description', 'requirements']
        df = df[column_order]
        
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
                
        df['due_date'] = df['due_date'].apply(lambda x: \
            (datetime.now().replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(extractRemainingTime(x))).timestamp())
        
        df['post_date'] = df['post_date'].apply(lambda x: \
            datetime.strptime(x, "%d/%m/%Y").timestamp())
        
        # Convert empty experience values to null
        df['experience'] = df['experience'].apply(lambda x: x if x != 'Không hiển thị' else None)
        
        # Save jobinfo dataframe
        self.save(df=df, output_path=output_path)
        
    def addCompanyImgUrls(self, jobinfo_path, joblist_path, output_path):
        jl_df = pd.read_json(joblist_path, encoding="utf-8")
        company_dict = dict(zip(jl_df['company'], jl_df['company_img_url']))
        
        df = pd.read_json(jobinfo_path, encoding="utf-8")
        df['company_img_url'] = df['company_name'].map(company_dict)
        
        # Reorder columns
        column_order = ['job_title', 'job_url', 'company_name', 'company_url', 'company_img_url', 'location', 'post_date', 'due_date',
                        'fields', 'salary', 'experience', 'position', 'benefits', 'job_description', 'requirements']
        df = df[column_order]
        
        self.save(df=df, output_path=output_path)
        
    def translateJobRequirements(self, jobinfo_path, output_path, job_idx=0):        
        df = pd.read_json(jobinfo_path, encoding="utf-8")
        
        if job_idx == 0:
            with open(output_path, 'a') as file:
                writer = csv.writer(file)
                writer.writerow(('job_title', 'company_name', 'requirements', 'requirements_language', 'en_requirements'))
        
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
    vnw_data_processor = VNWDataProcessor()
    
    job_segments_dir='vietnamworks/rawdata/jobinfo/segments'
    jobinfo_path='vietnamworks/rawdata/jobinfo/vnw_jobinfo_full.json'
    preprocessed_jobinfo_path='vietnamworks/data/vnw_jobinfo_full.json'
    joblist_path='vietnamworks/rawdata/joblist/vnw_joblist_full_url.json'
    url_jobinfo_path='vietnamworks/data/vnw_jobinfo_full_url.json'
    translation_path='vietnamworks/rawdata/translation/job_req_translation.csv'
    final_jobinfo_path='vietnamworks/data/preprocessed_jobinfo_full.json'
    
    # vnw_data_processor.mergeJobSegments(job_segments_dir=job_segments_dir,
    #                                 output_path=jobinfo_path,
    #                                 drop_duplicates=False)
    
    # vnw_data_processor.restructureJobInfo(jobinfo_path=jobinfo_path, output_path=preprocessed_jobinfo_path)
     
    # vnw_data_processor.addCompanyImgUrls(jobinfo_path=preprocessed_jobinfo_path, joblist_path=joblist_path, output_path=url_jobinfo_path)
    
    # vnw_data_processor.translateJobRequirements(jobinfo_path=url_jobinfo_path, output_path=translation_path, job_idx=9211)
    
    vnw_data_processor.addTranslationToJobInfo(jobinfo_path=url_jobinfo_path, translation_path=translation_path, output_path=final_jobinfo_path)