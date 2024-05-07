from rest_framework import serializers
from datetime import datetime

from .models import User

class UserSerializer(serializers.Serializer):
  uid = serializers.CharField()
  email = serializers.EmailField()
  username = serializers.CharField()
  cv_filename = serializers.CharField(default=None)
  created_at = serializers.DateTimeField(default=datetime.now())
  modified_at = serializers.DateTimeField(default=None)
  deleted = serializers.BooleanField(default=False)

  def create(self):
    self.is_valid(raise_exception=True)
    return User(**self.data)

