import pyrebase
import requests

from .config import FIREBASE_CONFIG
from .models import *
from .serializers import *
from .utils import generate_avatar

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
    Upload a file to storage
    '''
    result = storage_client.child(f'user/{user_id}/{filename}').put(data, token)
    return result
  
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
