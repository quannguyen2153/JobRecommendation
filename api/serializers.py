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
