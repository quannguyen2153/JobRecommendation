from rest_framework.authentication import BaseAuthentication
from rest_framework import exceptions

from .firebase import AuthHelper

class FirebaseAuthentication(BaseAuthentication):
  def authenticate(self, request):
    try:
      token = request.headers['Authorization']
      return (AuthHelper.verify_token(request.headers['Authorization']), token)
    except Exception as e:
      raise exceptions.AuthenticationFailed("Permission denied.")
