from django.http import HttpResponseRedirect
from rest_framework.views import APIView
from rest_framework.response import Response
import json

from .forms import *
from .firebase import UserResourceManager, AuthHelper
from .serializers import *
from .authenticate import FirebaseAuthentication

class SignUpView(APIView):
  '''
  Sign up with email and password
  '''
  http_method_names = ['post', 'options']

  def post(self, request):
    # Get data from request
    try:
      form = SignUpForm(json.loads(request.body))
      if not form.is_valid():
        raise Exception(form.errors.as_data())
    except Exception as e:
      return Response(
        data={
          "success": False, 
          "message": str(e)
        }, 
        status=400
      )

    # Register user
    try:
      AuthHelper.sign_up(form.data['email'], form.data['password'], form.data['username'])
    except Exception as e:
      return Response(
        data={
          "success": False, 
          "message": str(e)
        }, 
        status=500
      )
    return Response(
      data={
        "success": True, 
        "message": "User registered successfully"
      }, 
      status=201
    )
  
class SignInView(APIView):
  '''
  Sign in with email and password
  '''
  http_method_names = ['post', 'options']
  
  def post(self, request):
    # Get data from request
    try:
      form = SignInForm(json.loads(request.body))
      if not form.is_valid():
        raise Exception(form.errors.as_data())
    except Exception as e:
      return Response(
        data={
          "success": False, 
          "message": str(e)
        }, 
        status=400
      )
    
    # Sign user in
    data = AuthHelper.sign_in(email=form.data['email'], password=form.data['password'])
    if data is None:
      return Response(
        data={
          "success": False, 
          "message": "Invalid email or password."
        }, 
        status=401
      )
    
    user_data, token = data
    return Response(
      data={
        "success": True,
        "message": "User signed in successfully",
        "data": user_data,
        "token": token,
      }, 
    )

class ForgotPasswordView(APIView):
  '''
  Send password reset email to user
  '''
  http_method_names = ['post', 'options']

  def post(self, request):
    # Get data from request
    try:
      form = ForgotPasswordForm(json.loads(request.body))
      if not form.is_valid():
        raise Exception(form.errors.as_data())
    except Exception as e:
      return Response(
        data={
          "success": False, 
          "message": str(e)
        }, 
        status=400
      )
    
    # Send password reset email
    try:
      AuthHelper.forgot_password(form.data['email'])
    except Exception as e:
      return Response(
        data={
          "success": False, 
          "message": str(e)
        }, 
        status=500
      )
    return Response(
      data={
        "success": True, 
        "message": "Password reset email sent successfully."
      }, 
    )

class UserCVView(APIView):
  '''
  Upload and get user's own CV
  '''
  http_method_names = ['get', 'post', 'options']
  authentication_classes = [FirebaseAuthentication]

  def get(self, request):
    try:
      download_url = UserResourceManager.get_url("cv.pdf", request.user.uid, request.auth)
    except Exception as e:
      return Response(
        data = {
          "success": False, 
          "message": str(e)
        }, 
        status=400
      )
    
    if download_url is None:
      return Response(
        data = {
          "success": False, 
          "message": "CV file not found."
        }, 
        status=404
      )
    return Response({
      "success": True,
      "data": {"download_url": download_url}}, 
    )

  def post(self, request):
    try:
      if 'file' not in request.FILES:
        raise Exception("No file uploaded.")
      cv_file = request.FILES['file']
      UserResourceManager.upload_file("cv.pdf", cv_file, request.user.uid, request.auth)
    except Exception as e:
      return Response(
        data={
          "success": False, 
          "message": str(e)
        }, 
        status=400
      )
    return Response({
      "success": True, 
      "message": "File uploaded successfully."
    })
  
class UserAvatarView(APIView):
  '''
  Get user's own avatar
  '''
  http_method_names = ['get', 'options']
  authentication_classes = [FirebaseAuthentication]

  def get(self, request):
    try:
      download_url = UserResourceManager.get_url("avatar.svg", request.user.uid, request.auth)
      return HttpResponseRedirect(download_url)
    except Exception as e:
      return Response(
        data = {
          "success": False, 
          "message": str(e)
        }, 
        status=400
      )