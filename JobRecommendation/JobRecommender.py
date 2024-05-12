from sentence_transformers import SentenceTransformer, util

import pandas as pd

class JobRecommender():
    def __init__(self) -> None:
        # self.model = SentenceTransformer("multi-qa-MiniLM-L6-cos-v1") # 0.6s
        self.model = SentenceTransformer("multi-qa-mpnet-base-dot-v1") # 1.8s
        
    def attachJobs(self, jobs):
        # Will be modified in the future for integration capability
        self.job_df = jobs
        
    def attachCV(self, cv_dict):
        self.cv = cv_dict        
        self.cv_text = self.extractCVDictToText()
        
        self.cv_text_encoded = self.model.encode(self.cv_text)
        
    def extractCVDictToText(self):
        extract_keys=['Candidate\'s Profession',
                      'Candidate\'s Date of Birth',
                      'Candidate\'s Address',
                      'Candidate\'s Skills',
                      'Candidate\'s Experiences',
                      'Candidate\'s Education',
                      'Candidate\'s Certificates']
        extracted_cv_dict = {}
        
        for key in extract_keys:
            extracted_cv_dict[key] = self.cv[key]
                
        cv_text = ''
        for key, value in extracted_cv_dict.items():
            if value is None or '\n' not in value:
                cv_text = cv_text + key + ": " + str(value) + "\n"
            else:
                lines = value.split('\n')
                for i in range(len(lines)):
                    if '\t' not in lines[i]:
                        lines[i] = '\t' + lines[i]
                value = '\n'.join(lines)
                cv_text = cv_text + key + ":\n" + value + '\n'
        
        return cv_text
    
    def computeJobsSimilarity(self, job_df):
        def computeSimilarity(row):
            requirements = row['requirements'] if row['requirements_language'] == 'en' else row['en_requirements']
            
            requirements_encoded = self.model.encode(requirements)
                        
            return util.dot_score(self.cv_text_encoded, requirements_encoded).item()

        # Compute similarity
        job_df['similarity'] = job_df.apply(computeSimilarity, axis=1)
        
        return job_df