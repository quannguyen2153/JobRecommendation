from django.views.generic.base import View
from django.http import HttpResponse
from django import forms
import json

from .firebase import firebase_client
from .serializers import UserSerializer
from .database import UserManager

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
      data = json.loads(request.body)
      
      # Validate request data
      form = self.PostForm(data)
      if not form.is_valid():
        raise Exception(form.errors.as_data())
      
      # Extract data
      email = data['email']
      password = data['password']
      username = data['username']
    except Exception as e:
      return HttpResponse(json.dumps({"success": False, "message": str(e)}), content_type="application/json", status=400)
    
    # Register user
    try:
      # Call firebase API
      result = firebase_client.auth().create_user_with_email_and_password(email=email, password=password)

      # Create user in database
      user_data = {
        "uid": result['localId'],
        "email": email,
        "username": username,
      }
      user = UserSerializer(data=user_data).create()
      UserManager.create(user)
    except Exception as e:
      response = {
        "success": False,
        "message": str(e),
      }
      return HttpResponse(json.dumps(response), content_type="application/json", status=500)
    
    response = {
      "success": True,
      "message": "User registered successfully",
    }
    return HttpResponse(json.dumps(response), content_type="application/json", status=201)
  
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
      data = json.loads(request.body)

      # Validate request data
      form = self.PostForm(data)
      if not form.is_valid():
        raise Exception(form.errors.as_data())
      
      # Extract data
      email = data['email']
      password = data['password']
    except Exception as e:
      return HttpResponse(json.dumps({"success": False, "message": str(e)}), content_type="application/json", status=400)
    
    # Sign in user
    try:
      # Call firebase API
      result = firebase_client.auth().sign_in_with_email_and_password(email=email, password=password)
    except Exception as e:
      response = {
        "success": False,
        "message": str(e),
      }
      return HttpResponse(json.dumps(response), content_type="application/json", status=500)
    
    user_data = UserSerializer(UserManager.get(result['localId'])).data
    response = {
      "success": True,
      "message": "User signed in successfully",
      "data": user_data,
    }
    httpResponse = HttpResponse(json.dumps(response), content_type="application/json", status=200)
    httpResponse.headers['Set-Cookie'] = f"idToken={result['idToken']}"
    return httpResponse