import requests

from .firebase import firebase_client
from .models import User
from .serializers import UserSerializer


database = firebase_client.database()
storage = firebase_client.storage()

class UserManager:
  @staticmethod
  def create(user):
    database.child("users").child(user.uid).set(UserSerializer(user).data)
    return

  @staticmethod
  def get(uid):
    user_data = database.child("users").child(uid).get().val()
    if user_data is None:
      return None
    return User(**user_data)
  
class UserResourceManager:
  @staticmethod
  def upload_file(filename, data, user_id, token):
    result = storage.child(f'user/{user_id}/{filename}').put(data, token)
    return result
  
  @staticmethod
  def get_url(filename, user_id, id_token):
    # Get download token
    r = requests.get(f'https://firebasestorage.googleapis.com/v0/b/{firebase_client.storage_bucket}/o/user%2F{user_id}%2F{filename}', 
                     headers={'Authorization': f'Bearer {id_token}'})
    if r.status_code == 200:
      download_token = r.json()['downloadTokens']
    else:
      return None
    
    # Get url
    url = storage.child(f'user/{user_id}/{filename}').get_url(download_token)
    return url