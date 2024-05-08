from django.views.generic.base import View
from django.http import JsonResponse, HttpResponse
from django import forms
import json

from .firebase import firebase_client
from .serializers import UserSerializer
from .database import UserManager, UserResourceManager
from .utils import authorization_required

def home(request):
  return HttpResponse("Hello!")

class SignUpView(View):
  '''
  Sign up with email and password
  '''
  def get(self, request): 
    return HttpResponse("GET method is not supported.", status=405)
  class PostForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField()
    username = forms.CharField()

  def post(self, request):
    # Get data from request
    try:
      # Validate and extract request data
      data = json.loads(request.body)
      form = self.PostForm(data)
      if not form.is_valid():
        raise Exception(form.errors.as_data())
    except Exception as e:
      return JsonResponse({"success": False, "message": str(e)}, status=400)

    # Register user
    try:
      # Call firebase API
      result = firebase_client.auth().create_user_with_email_and_password(email=form.data['email'], password=form.data['password'])
      # Create user in database
      user = UserSerializer(data={
        "uid": result['localId'],
        "email": result['email'],
        "username": form.data['username'],
      }).create()
      UserManager.create(user)
    except Exception as e:
      return JsonResponse({"success": False, "message": str(e)}, status=500)
    return JsonResponse({"success": True, "message": "User registered successfully",}, status=201)
  
class SignInView(View):
  '''
  Sign in with email and password
  '''
  def get(self, request): 
    return HttpResponse("GET method is not supported.", status=405)
  
  class PostForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField()
  
  def post(self, request):
    # Get data from request
    try:
      # Validate and extract request data
      data = json.loads(request.body)
      form = self.PostForm(data)
      if not form.is_valid():
        raise Exception(form.errors.as_data())
    except Exception as e:
      return JsonResponse({"success": False, "message": str(e)}, status=400)
    
    # Sign in user
    try:
      # Call firebase API
      result = firebase_client.auth().sign_in_with_email_and_password(email=form.data['email'], password=form.data['password'])
    except Exception as e:
      return JsonResponse({"success": False, "message": str(e)}, status=500)
    
    user_data = UserSerializer(UserManager.get(result['localId'])).data
    response = JsonResponse({
      "success": True,
      "message": "User signed in successfully",
      "data": user_data,
    }, status=200)
    response.headers['Set-Cookie'] = f"idToken={result['idToken']};refreshToken={result['refreshToken']};"
    return response

class UserCVView(View):
  '''
  Upload and get user's own CV
  '''

  @authorization_required
  def get(self, request, user=None, id_token=None):
    try:
      download_url = UserResourceManager.get_url("cv.pdf", user.uid, id_token)
    except Exception as e:
      return JsonResponse({"success": False, "message": str(e)}, status=400)
    
    if download_url is None:
      return JsonResponse({"success": False, 
                           "message": "CV file not found."}, 
                          status=404)
    return JsonResponse({"success": True, 
                         "message": "Get CV successfully.",
                         "data": {"download_url": download_url}}, 
                        status=200)

  @authorization_required
  def post(self, request, user=None, id_token=None):
    try:
      if 'file' not in request.FILES:
        raise Exception("No file uploaded.")
      cv_file = request.FILES['file']
      UserResourceManager.upload_file("cv.pdf", cv_file, user.uid, id_token)
    except Exception as e:
      return JsonResponse({"success": False, "message": str(e)}, status=400)
    return JsonResponse({"success": True, "message": "File uploaded successfully."}, status=200)