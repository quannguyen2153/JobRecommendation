import os
import pandas as pd
import json

class VNWDataProcessor():
    def __init__(self) -> None:
        pass
        
    def mergeJobList(self, joblist_dir, output_path):
        dfs = []
        for filename in os.listdir(joblist_dir):
            if filename.endswith(".json"):
                file_path = os.path.join(joblist_dir, filename)
                df = pd.read_json(file_path, encoding="utf-8")
                dfs.append(df)

        merged_df = pd.concat(dfs, ignore_index=True).drop_duplicates()
        
        merged_df.to_json(output_path, orient="records", indent=4, force_ascii=False)
        print('Wrote {} jobs to {}.'.format(merged_df.shape[0], output_path))
        
if __name__ == '__main__':
    vnw_data_processor = VNWDataProcessor()
    vnw_data_processor.mergeJobList(joblist_dir='vietnamworks/rawdata/joblist/segments',
                                    output_path='vietnamworks/rawdata/joblist/vnw_joblist_full.json')