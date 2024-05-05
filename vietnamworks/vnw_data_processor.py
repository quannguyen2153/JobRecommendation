import os
import pandas as pd
import json

from googletrans import Translator

import re
import time
from datetime import datetime, timedelta

class VNWDataProcessor():
    def __init__(self) -> None:
        self.translator = Translator()
        
    def save(self, df, output_path):
        df.to_json(output_path, orient="records", indent=4, force_ascii=False)
        print('Wrote {} jobs to {}.'.format(df.shape[0], output_path))
        
    def checkLanguages(self, file_path, output_path):
        def detectLanguage(text):
            time.sleep(1)
            detected_lang = self.translator.detect(text).lang
            print(detected_lang)
            return detected_lang
        
        df = pd.read_json(file_path, encoding="utf-8")
        df['lang'] = df['title'].apply(lambda x: detectLanguage(x))
        
        self.save(df=df, output_path=output_path)
        
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
        
        # Merge requirements with skills
        df['requirements'] = df['requirements'] + '\n' + df['skills']
        
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
        
    def translateText(self, org_text, src_lng, dst_lng, retries=5, truncation_length=30):
        def truncateText(text):
            if '\n' in text[:truncation_length]:
                truncated_index = text[:truncation_length].index('\n')
                return text[:truncated_index].strip() + '...'
            else:
                if len(text) > truncation_length:
                    return text[:truncation_length-3].strip() + '...'
                else:
                    return text.strip()
                
        print('\"{:<{}}\"'.format(truncateText(org_text), truncation_length), end=' ')
        
        for i in range(retries-1):
            time.sleep(2**i)
            
            try:
                if len(org_text.strip()) == 0 or self.translator.detect(org_text).lang == dst_lng:
                    print('{:^13} \"{:<{}}\"'.format('remains', truncateText(org_text), truncation_length))
                    return org_text
                                
                translated_text = self.translator.translate(org_text, src=src_lng, dest=dst_lng).text
                
                print('{:^13} \"{:<{}}\"'.format('translated to', truncateText(translated_text), truncation_length))                
                return translated_text
            except:
                print('retrying', end=' ')
                continue
            
        time.sleep(2**retries)
        
        if len(org_text.strip()) == 0 or self.translator.detect(org_text).lang == dst_lng:
            print('{:^13} \"{:<{}}\"'.format('remains', truncateText(org_text), truncation_length))
            return org_text
                        
        translated_text = self.translator.translate(org_text, src=src_lng, dest=dst_lng).text
                
        print('{:^13} \"{:<{}}\"'.format('translated to', truncateText(translated_text), truncation_length))                
        return translated_text
    
    def translateTextList(self, text_list, src_lng, dst_lng):
        return [self.translateText(text, src_lng, dst_lng) for text in text_list]
        
    def translateJobInfo(self, jobinfo_df, src_lng, dst_lng):
        translated_df = pd.DataFrame()
        
        for column in jobinfo_df.columns:
            if column == 'post_date' or column == 'location' or column == 'company' or column == 'contact':
                translated_df[column] = jobinfo_df[column]
                print('Skipped {}.'.format(column))
                continue
            
            print('Translating {}...'.format(column))
            
            if isinstance(jobinfo_df[column].iloc[0], list):
                translated_column = jobinfo_df[column].apply(lambda x: self.translateTextList(x, src_lng, dst_lng))
            else:
                translated_column = jobinfo_df[column].apply(lambda x: self.translateText(x, src_lng, dst_lng))
            translated_df[column] = translated_column
            
        return translated_df
    
    def calculateEndDate(self, jobinfo_df):
        def extractDays(end_date_str):
            days = re.search(r'(\d+)\s+day', end_date_str)
            if days:
                return int(days.group(1))
            else:
                return 0
            
        def calculateEndDate(end_date_str):
            days = extractDays(end_date_str)
            return (datetime.today() + timedelta(days=days)).strftime('%d/%m/%Y')
        
        jobinfo_df['end_date'] = jobinfo_df['end_date'].apply(calculateEndDate)
        
        return jobinfo_df

        
if __name__ == '__main__':
    vnw_data_processor = VNWDataProcessor()
    
    job_segments_dir='vietnamworks/rawdata/jobinfo/segments'
    jobinfo_path='vietnamworks/rawdata/jobinfo/vnw_jobinfo_full.json'
    preprocessed_jobinfo_path='vietnamworks/data/vnw_jobinfo_full.json'
    
    # vnw_data_processor.mergeJobSegments(job_segments_dir=job_segments_dir,
    #                                 output_path=jobinfo_path,
    #                                 drop_duplicates=False)
    
    vnw_data_processor.restructureJobInfo(jobinfo_path=jobinfo_path, output_path=preprocessed_jobinfo_path)
    