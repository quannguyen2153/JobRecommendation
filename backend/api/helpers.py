from datetime import datetime

from api.serializers import CVFileInfoSerializer, CVDataSerializer, \
  SessionSerializer, UserSerializer
from api.firebase import auth_client, SessionDataManager, UserManager, \
  UserResourceManager, CVManager, JobManager, JobRecommenderDataManager
from api.utils import convert_size, generate_avatar

from ai_models.JobChatBot import JobChatBot
from ai_models.CVParser import CVParser
import ai_models.JobRecommender as JobRecommender

from config.config import JOB_PAGE_SIZE

class CVHelper:
  '''
  Helper class for uploading and processing CV
  '''
  @staticmethod
  def get_cv_file_info(user_id):
    '''
    Get CV file info by user_id
    Return: file_info
    '''
    return CVManager.get_cv_file_info(user_id)

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
    session = SessionSerializer(data={
      'id_token': result['idToken'],
      'refresh_token': result['refreshToken']
    }).create()
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
    if recommended_job_ids is None:
      raise Exception("No recommendations found. Please upload your CV first.")
    total = len(recommended_job_ids)
    if page is None:
      return JobManager.get_jobs(recommended_job_ids), total
    else:
      start = (page - 1) * JOB_PAGE_SIZE
      end = page * JOB_PAGE_SIZE
      return JobManager.get_jobs(recommended_job_ids[start:end]), total