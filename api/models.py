from datetime import datetime

class SessionData:
  '''
  Class to store id_token and refresh_token from Firebase
  '''
  def __init__(self, id_token, refresh_token):
    self.id_token = id_token
    self.refresh_token = refresh_token

class UserData:
  def __init__(self, uid, email, username, created_at=None, modified_at=None, deleted=None):
    self.uid = uid
    self.email = email
    self.username = username
    self.created_at = created_at or datetime.now()
    self.modified_at = modified_at or datetime.now()
    self.deleted = deleted

