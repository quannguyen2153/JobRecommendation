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
    # vnw_data_processor.mergeJobSegments(job_segments_dir='vietnamworks/rawdata/jobinfo/segments',
    #                                 output_path='vietnamworks/rawdata/jobinfo/vnw_jobinfo_full.json')
    
    df = pd.read_json('vietnamworks/rawdata/jobinfo/segments/vnw_jobinfo_500.json', encoding="utf-8")
    
    translated_df = vnw_data_processor.translateJobInfo(df, 'auto', 'en')    
    vnw_data_processor.save(df=translated_df, output_path='vietnamworks/rawdata/jobinfo/translated_jobinfo_500.json')
    
    # df = vnw_data_processor.calculateEndDate(jobinfo_df=df)
    # vnw_data_processor.save(df=df, output_path='vietnamworks/rawdata/jobinfo/preprocessed_jobinfo.json')