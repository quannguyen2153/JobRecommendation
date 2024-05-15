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

class CVSerializer(serializers.Serializer):
  profession = serializers.CharField(source="Candidate's Profession", required=False)
  name = serializers.CharField(source="Candidate's Name", required=False)
  dob = serializers.CharField(source="Candidate's Date of Birth", required=False)
  phone = serializers.CharField(source="Candidate's Phone", required=False)
  address = serializers.CharField(source="Candidate's Address", required=False)
  email = serializers.CharField(source="Candidate's Email", required=False)
  website = serializers.CharField(source="Candidate's Website", required=False)
  skills = serializers.CharField(source="Candidate's Skills", required=False)
  experiences = serializers.CharField(source="Candidate's Experiences", required=False)
  education = serializers.CharField(source="Candidate's Education", required=False)
  certificates = serializers.CharField(source="Candidate's Certificates", required=False)
  references = serializers.CharField(source="Candidate's References", required=False)

  def create(self):
    return CVData(**self.data)