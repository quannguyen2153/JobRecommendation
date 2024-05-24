import pyrebase
import requests

from config.config import FIREBASE_CONFIG
from .models import *
from .serializers import *

firebase_client = pyrebase.initialize_app(FIREBASE_CONFIG)

auth_client = firebase_client.auth()
database_client = firebase_client.database()
storage_client = firebase_client.storage()

class SessionDataManager:
  @staticmethod
  def create(session):
    '''
    Create a new session data in database
    '''
    database_client.child("sessions").push(SessionSerializer(session).data)
    return

  @staticmethod
  def get_refresh_token(id_token):
    '''
    Get corresponding refresh token from database
    '''
    result = database_client.child("sessions").order_by_child('id_token').equal_to(id_token).get().val()
    _, data = list(result.items())[0]
    refresh_token = data['refresh_token']
    return refresh_token

class UserManager:
  @staticmethod
  def create(user):
    '''
    Create a new user in database
    '''
    database_client.child("users").child(user.uid).set(UserSerializer(user).data)
    return

  @staticmethod
  def get(uid):
    '''
    Get user by uid from database
    '''
    user_data = database_client.child("users").child(uid).get().val()
    if user_data is None:
      return None
    return UserData(**user_data)
  
class UserResourceManager:
  @staticmethod
  def upload_file(filename, data, user_id, token):
    '''
    Upload a file to storage and return download url
    '''
    path = f'user/{user_id}/{filename}'
    result = storage_client.child(path).put(data, token)
    download_url = storage_client.child(path).get_url(result['downloadTokens'])
    return download_url
  
  @staticmethod
  def get_url(filename, user_id, id_token):
    '''
    Get download url for a file from storage
    '''
    # Get download token
    r = requests.get(f'https://firebasestorage.googleapis.com/v0/b/{firebase_client.storage_bucket}/o/user%2F{user_id}%2F{filename}', 
                     headers={'Authorization': f'Bearer {id_token}'})
    if r.status_code == 200:
      download_token = r.json()['downloadTokens']
    else:
      return None
    
    # Get url
    url = storage_client.child(f'user/{user_id}/{filename}').get_url(download_token)
    return url

class CVManager:
  @staticmethod
  def create(cv_data, file_info, user_id):
    '''
    Create a new CV in database
    '''
    database_client.child("cv_data").child(user_id).set(cv_data.__dict__)
    database_client.child("cv_file_info").child(user_id).set(file_info.__dict__)
    print("CV data and file info saved to database.")
    return

  @staticmethod
  def get_cv_data(user_id):
    '''
    Get CV data by user_id from database
    '''
    cv_data = database_client.child("cv_data").child(user_id).get().val()
    if cv_data is None:
      return None
    return CVData(**cv_data)

  @staticmethod
  def get_cv_file_info(user_id):
    '''
    Get CV file info by user_id from database
    '''
    file_info = database_client.child("cv_file_info").child(user_id).get().val()
    if file_info is None:
      return None
    return CVFileInfo(**file_info)


class JobManager:
  @staticmethod
  def get_all_jobs():
    '''
    Get all jobs from database
    '''
    jobs = database_client.child("jobs").get().val()
    return [JobData(**job) for job in jobs.values()]

  @staticmethod
  def get_job(job_id):
    '''
    Get jobs by id from database
    '''
    return JobData(**database_client.child("jobs").child(job_id).get().val())

  @staticmethod
  def get_jobs(job_ids):
    '''
    Get jobs by ids from database
    '''
    return [JobData(**database_client.child("jobs").child(id).get().val()) for id in job_ids]

class JobRecommenderDataManager:
  @staticmethod
  def get_recommendations(user_id):
    '''
    Get job recommendations by user_id from database
    '''
    return database_client.child("recommendations").child(user_id).get().val()
  
  @staticmethod
  def save_recommendations(user_id, job_ids):
    '''
    Create job recommendations in database
    '''
    database_client.child("recommendations").child(user_id).set(job_ids)
    return
