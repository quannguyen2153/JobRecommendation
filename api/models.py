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

class JobData:
  def __init__(self, id, job_title=None, job_url=None, company_name=None, company_url=None, company_img_url=None, 
               location=None, post_date=None, due_date=None, fields=None, salary=None, position=None, 
               benefits=None, experience=None, job_description=None, requirements=None):
    self.id = id
    self.job_title = job_title
    self.job_url = job_url
    self.company_name = company_name
    self.company_url = company_url
    self.company_img_url = company_img_url
    self.location = location
    self.post_date = post_date
    self.due_date = due_date
    self.fields = fields
    self.salary = salary
    self.position = position
    self.benefits = benefits
    self.experience = experience
    self.job_description = job_description
    self.requirements = requirements

class CVData:
  '''
  Class to store parsed CV data
  '''
  def __init__(self, profession = None, name = None, dob = None, phone = None, 
               address = None, email = None, website = None, skills = None, 
               experiences = None, education = None, certificates = None, references = None):
    self.profession = profession
    self.name = name
    self.dob = dob
    self.phone = phone
    self.address = address
    self.email = email
    self.website = website
    self.skills = skills
    self.experiences = experiences
    self.education = education
    self.certificates = certificates
    self.references = references

class CVFileInfo:
  '''
  Class to store CV file information
  '''
  def __init__(self, file_name, file_size, file_url, uploaded_at):
    self.file_name = file_name
    self.file_size = file_size
    self.file_url = file_url
    self.uploaded_at = uploaded_at
