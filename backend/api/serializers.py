from rest_framework import serializers
from datetime import datetime
from .models import *

class SessionSerializer(serializers.Serializer):
  id_token = serializers.CharField()
  refresh_token = serializers.CharField()
  
  def create(self):
    self.is_valid(raise_exception=True)
    return SessionData(**self.data)

class UserSerializer(serializers.Serializer):
  uid = serializers.CharField()
  email = serializers.EmailField()
  username = serializers.CharField()
  created_at = serializers.DateTimeField(default=datetime.now())
  modified_at = serializers.DateTimeField(default=None)
  deleted = serializers.BooleanField(default=False)

  def create(self):
    self.is_valid(raise_exception=True)
    return UserData(**self.data)

class JobSerializer(serializers.Serializer):
  id = serializers.IntegerField(min_value=1, required=True)
  job_title = serializers.CharField()
  job_url = serializers.URLField()
  company_name = serializers.CharField()
  company_url = serializers.URLField()
  company_img_url = serializers.URLField()
  location = serializers.CharField()
  post_date = serializers.IntegerField()
  due_date = serializers.IntegerField()
  fields = serializers.CharField()
  salary = serializers.CharField()
  position = serializers.CharField()
  benefits = serializers.CharField()
  experience = serializers.CharField()
  job_description = serializers.CharField()
  requirements = serializers.CharField()
  
  def create(self):
    self.is_valid(raise_exception=True)
    return JobData(**self.data)

class CVDataSerializer(serializers.Serializer):
  profession = serializers.CharField(source="Profession", required=False)
  name = serializers.CharField(source="Name", required=False)
  dob = serializers.CharField(source="Date of Birth", required=False)
  phone = serializers.CharField(source="Phone", required=False)
  address = serializers.CharField(source="Address", required=False)
  email = serializers.CharField(source="Email", required=False)
  website = serializers.CharField(source="Website", required=False)
  skills = serializers.CharField(source="Skills", required=False)
  experiences = serializers.CharField(source="Experiences", required=False)
  education = serializers.CharField(source="Education", required=False)
  certificates = serializers.CharField(source="Certificates", required=False)
  references = serializers.CharField(source="References", required=False)

  def create(self):
    return CVData(**self.data)
  
class CVFileInfoSerializer(serializers.Serializer):
  file_name = serializers.CharField()
  file_size = serializers.CharField()
  file_url = serializers.URLField()
  uploaded_at = serializers.IntegerField()

  def create(self):
    self.is_valid(raise_exception=True)
    return CVFileInfo(**self.data)