from sentence_transformers import SentenceTransformer, util

import pandas as pd

class JobRecommender():
    def __init__(self) -> None:
        self.model = SentenceTransformer("multi-qa-mpnet-base-dot-v1")
        
    def attachJobs(self, job_df):
        self.job_df = job_df
        
    def attachCV(self, cv_dict):
        self.cv = cv_dict        
        self.cv_text = self.extractCVDictToText()
        
        self.cv_text_encoded = self.model.encode(self.cv_text)
        
    def extractCVDictToText(self):
        extract_keys=['Candidate\'s Profession',
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
    
    def computeJobsSimilarity(self):
        # Compute similarity
        similarity_job_df = self.job_df.copy(deep=True)
        similarity_job_df['similarity'] = similarity_job_df['req_vector'] \
                                            .apply(lambda x: util.dot_score(self.cv_text_encoded, x).item())
        
        return similarity_job_df