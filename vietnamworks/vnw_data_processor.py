import os
import pandas as pd
import json

from googletrans import Translator

class VNWDataProcessor():
    def __init__(self) -> None:
        self.translator = Translator()
        
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
        
        merged_df.to_json(output_path, orient="records", indent=4, force_ascii=False)
        print('Wrote {} jobs to {}.'.format(merged_df.shape[0], output_path))
        
    def translateText(self, text, src_lng, dst_lng):
        if len(text.strip()) == 0 or self.translator.detect(text).lang == dst_lng:
            return text
        
        return self.translator.translate(text, src=src_lng, dest=dst_lng).text
    
    def translateTextList(self, text_list, src_lng, dst_lng):
        return [self.translateText(text, src_lng, dst_lng) for text in text_list]
        
    def translateJobInfo(self, jobinfo_df, src_lng, dst_lng):
        translated_df = pd.DataFrame()
        
        for column in jobinfo_df.columns:
            if column == 'post_date' or column == 'location' or column == 'company' or column == 'contact':
                print('Skipped {}.'.format(column))
                continue
            
            print('Translating {}...'.format(column))
            
            if isinstance(jobinfo_df[column].iloc[0], list):
                translated_column = jobinfo_df[column].apply(lambda x: self.translateTextList(x, src_lng, dst_lng))
            else:
                translated_column = jobinfo_df[column].apply(lambda x: self.translateText(x, src_lng, dst_lng))
            translated_df[column] = translated_column
            
        return translated_df

        
if __name__ == '__main__':
    vnw_data_processor = VNWDataProcessor()
    # vnw_data_processor.mergeJobSegments(job_segments_dir='vietnamworks/rawdata/jobinfo/segments',
    #                                 output_path='vietnamworks/rawdata/jobinfo/vnw_jobinfo_full.json')
    
    df = pd.read_json('vietnamworks/rawdata/jobinfo/segments/vnw_jobinfo_500.json', encoding="utf-8")
    
    translated_df = vnw_data_processor.translateJobInfo(df, 'auto', 'en')
    
    print(translated_df.iloc[:5])