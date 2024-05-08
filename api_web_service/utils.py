from django.http import JsonResponse
import json

from .database import UserManager
from .firebase import firebase_client

def authorization_required(f):
  '''
  Decorator to check if the request is authorized
  '''
  def wrapper(*args, **kwargs):
    request = args[1]
    if 'HTTP_COOKIE' not in request.META:
      return JsonResponse({"success": False, "message": "Authorization required"}, status=401)
    
    # Get authorize cookies
    cookies = request.META['HTTP_COOKIE']
    cookies = cookies.split(';')
    id_token = None
    refresh_token = None
    for cookie in cookies:
      if cookie.startswith('idToken='):
        id_token = cookie.split('=')[1]
      if cookie.startswith('refreshToken='):
        refresh_token = cookie.split('=')[1]
    
    if id_token is None or refresh_token is None:
      return JsonResponse({"success": False, "message": "Permission denied."}, status=401)
    
    try:
      # Verify token
      user_id = firebase_client.auth().get_account_info(id_token)['users'][0]['localId']
      r = firebase_client.auth().refresh(refresh_token)
      firebase_client.auth().get_account_info(id_token)

      # Add parameters then call the wrapped function
      user = UserManager.get(user_id)
      kwargs['user'] = user
      kwargs['id_token'] = id_token
      return f(*args, **kwargs)
    except Exception as e:
      return JsonResponse(json.dumps({"success": False, "message": str(e)}), status=401)
    
  
  return wrapper

