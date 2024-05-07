from .firebase import firebase_client
from .models import User
from .serializers import UserSerializer

database = firebase_client.database()

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
  