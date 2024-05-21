import pyrebase
import requests

from .config import FIREBASE_CONFIG, PAGE_SIZE
from .models import *
from .serializers import *
from .utils import generate_avatar, convert_size
from ai_models.CVParser import CVParser
from ai_models.JobChatBot import JobChatBot
import ai_models.JobRecommender as JobRecommender

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
  
  @staticmethod
  def get_job_dummy(list_ids, page):
    '''
    Get jobs dummy
    '''
    start = (page - 1) * PAGE_SIZE
    end = page * PAGE_SIZE
    return JobManager.get_jobs(list_ids[start:end])

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

class CVHelper:
  '''
  Helper class for uploading and processing CV
  '''
  @staticmethod
  def upload_and_process_cv(file, user_id, token):
    '''
    Upload CV file to storage and process it
    return: file_info
    '''
    file_name = file.name
    if not file_name.endswith(".pdf"):
      raise Exception("Invalid file type. Only PDF files are supported.")
    if len(file_name) > 40:
      raise Exception("File name too long.")

    data = file.read()
    file_size = convert_size(len(data))
    # Upload file to storage
    download_url = UserResourceManager.upload_file("cv.pdf", data, user_id, token)
    if download_url is None:
      raise Exception("Failed to upload file.")
    file_info = CVFileInfoSerializer(data={
      "file_name": file_name,
      "file_size": file_size,
      "file_url": download_url,
      "uploaded_at": int(datetime.now().timestamp())
    }).create()
    
    # Process CV data and save results to database
    parsed_data = CVParser.parse_cv(data)
    cv = CVDataSerializer(parsed_data).create()
    CVManager.create(cv, file_info, user_id)

    recommended_jobs = JobRecommender.recommend_jobs(cv.__dict__)
    JobRecommenderDataManager.save_recommendations(user_id, recommended_jobs)

    return file_info

class ChatBotHelper:
  @staticmethod
  def send_message(user_id, job_id, message):
    '''
    Send message to chatbot
    '''
    user_cv = CVManager.get_cv_data(user_id)
    job = JobManager.get_job(job_id)
    return JobChatBot.send_message(cv_dict=user_cv.__dict__, job_dict=job.__dict__, message=message) 

class AuthHelper:
  @staticmethod
  def sign_up(email, password, username):
    """
    Sign up with email and password
    """
    result = auth_client.create_user_with_email_and_password(email, password)

    # Create user object in database
    user = UserSerializer(data={
      "uid": result['localId'],
      "email": email,
      "username": username,
    }).create()
    UserManager.create(user)
    
    # Generate avatar for new user
    avatar = generate_avatar().encode()
    UserResourceManager.upload_file("avatar.svg", avatar, result['localId'], result['idToken'])
  
  @staticmethod
  def sign_in(email, password):
    """
    Sign in with email and password
    Return: user_data and token if sign in is successful, None otherwise
    """
    try:
      result = auth_client.sign_in_with_email_and_password(email, password)
    except:
      return None
    
    # Store session data object in database
    session = SessionData(result['idToken'], result['refreshToken'])
    SessionDataManager.create(session)
    
    user_data = UserSerializer(UserManager.get(result['localId'])).data
    return user_data, result['idToken']

  @staticmethod
  def verify_token(id_token):
    """
    Verify id token, then refresh user session
    Return: user object if token is valid, raise exception otherwise
    """
    user_id = auth_client.get_account_info(id_token)['users'][0]['localId']
    refresh_token = SessionDataManager.get_refresh_token(id_token)
    auth_client.refresh(refresh_token)
    return UserManager.get(user_id)
    
  @staticmethod
  def forgot_password(email):
    """
    Send reset password email to user
    """
    auth_client.send_password_reset_email(email)
    return

class JobHelper:
  @staticmethod
  def get_recommended_jobs(user_id, page = None):
    '''
    Get recommended jobs by user_id
    Return: jobs in requested page, total number of jobs
    '''
    recommended_job_ids = JobRecommenderDataManager.get_recommendations(user_id)
    
    total = len(recommended_job_ids)
    if page is None:
      return JobManager.get_jobs(recommended_job_ids), total
    else:
      start = (page - 1) * PAGE_SIZE
      end = page * PAGE_SIZE
      return JobManager.get_jobs(recommended_job_ids[start:end]), total