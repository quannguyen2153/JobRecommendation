from datetime import datetime

class User:
  def __init__(self, uid, email, username, created_at=None, modified_at=None, deleted=None):
    self.uid = uid
    self.email = email
    self.username = username
    self.created_at = created_at or datetime.now()
    self.modified_at = modified_at or datetime.now()
    self.deleted = deleted
