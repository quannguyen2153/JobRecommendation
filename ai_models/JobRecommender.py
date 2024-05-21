from sentence_transformers import SentenceTransformer, util
import pandas as pd

class JobRecommender():
    def __init__(self) -> None:
        self.model = SentenceTransformer("multi-qa-mpnet-base-dot-v1")        
        
    def attachFields(self, field_df):
        self.field_df = field_df        
        
    def attachJobs(self, job_df):
        self.job_df = job_df
        
    def attachCV(self, cv_dict):
        self.cv = cv_dict        
        self.cv_text = self.extractCVDictToText()
        self.cv_profession_encoded = self.model.encode(self.cv['profession'])
        self.cv_text_encoded = self.model.encode(self.cv_text)
        
    def extractCVDictToText(self):
        extract_keys=[('Profession', 'profession'),
                      ('Skills', 'skills'),
                      ('Experiences', 'experiences'),
                      ('Education', 'education'),
                      ('Certificates', 'certificates')]
        extracted_cv_dict = {}
        
        for dst_key, src_key in extract_keys:
            extracted_cv_dict[dst_key] = self.cv[src_key]
                
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
    
    def computeJobsSimilarity(self, sort=True, top_f=2):
        # Field similarity
        similarity_field_df = self.field_df.copy(deep=True)
        similarity_field_df['similarity'] = similarity_field_df['field_vector'] \
                                            .apply(lambda x: util.dot_score(self.cv_profession_encoded, x).item())                                            
        similarity_field_df = similarity_field_df.sort_values(by='similarity', ascending=False)
        desc_similar_fields = similarity_field_df['field'].head(top_f).values.tolist()
        
        # Job similarity
        similarity_job_df = self.job_df.copy(deep=True)
        similarity_job_df = similarity_job_df[similarity_job_df['en_fields'].apply(lambda x: any(item in desc_similar_fields for item in x))]
        similarity_job_df['similarity'] = similarity_job_df['req_vector'] \
                                            .apply(lambda x: util.dot_score(self.cv_text_encoded, x).item())
                                            
        if sort:
            similarity_job_df = similarity_job_df.sort_values(by='similarity', ascending=False)
        
        return similarity_job_df
    

print("Initializing Job Recommender")

job_df = pd.read_json('data/jobs.json', encoding="utf-8")
field_df = pd.read_json('data/encoded_fields.json', encoding="utf-8") 

job_recommender = JobRecommender()
job_recommender.attachJobs(job_df=job_df)
job_recommender.attachFields(field_df=field_df)

print("Job Recommender initialized")

def recommend_jobs(cv_dict):
  '''
  Recommend jobs based on CV
  Return list of job ids
  '''
  try:
    job_recommender.attachCV(cv_dict=cv_dict)
    similarity_job_df = job_recommender.computeJobsSimilarity(sort=True, top_f=2)
    return similarity_job_df['id'].values.tolist()
  except Exception as e:
    raise Exception(f"Failed to recommend jobs: {str(e)}")
