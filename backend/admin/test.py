import requests
import random

ID = random.randbytes(8).hex()
URL = "http://localhost:8000/api/"
USER_NAME = f"test{ID}@gmail.com"
PASSWORD = "test123"
TOKEN = ""

def sign_up(email, password, username):
    url = URL + "signup/"
    headers = {
        "Content-Type": "application/json"
    }
    data = {
        "email": email,
        "password": password,
        "username": username
    }
    response = requests.post(url, headers=headers, json=data)
    print(response.json())

    return response.json()

def sign_in(email, password):
    url = URL + "signin/"
    headers = {
        "Content-Type": "application/json"
    }
    data = {
        "email": email,
        "password": password
    }
    response = requests.post(url, headers=headers, json=data)
    
    print(response.json())

    global TOKEN
    TOKEN = response.json()['token']
    return response.json()

def test_upload_file():
    url = URL + "user/cv/"
    files = {"file": open("sample_cv.pdf", "rb")}
    headers = {
      "Authorization": TOKEN
    }
    response = requests.post(url, headers=headers, files=files)
    print(response.json())
    return response.json()

def test_get_cv_file():
    url = URL + "user/cv/"
    headers = {
      "Authorization": TOKEN
    }
    response = requests.get(url, headers=headers)
    print(response.json())
    return response.json()

def test_forgot_password(email):
    url = URL + "forgot-password/"
    data = {
        "email": email
    }
    response = requests.post(url, json=data)
    print(response.json())

    return response.json()

def test_get_avatar():
    url = URL + "user/avatar/"
    headers = {
      "Authorization": TOKEN
    }
    response = requests.get(url, headers=headers)
    print(response.text)
    return response.text

def test_get_jobs():
    url = URL + "jobs/"
    headers = {
      "Authorization": TOKEN
    }
    response = requests.get(url, headers=headers)
    print(response.json())
    return response.json()

def test_chatbot():
    url = URL + "chatbot/"
    headers = {
      "Authorization": TOKEN
    }
    data = {
      "job_id": 1,
      "message": "I am a software engineer with 5 years of experience in Python and Java."
    }
    response = requests.post(url, headers=headers, json=data)
    print(response.json())
    return response.json()


sign_up(USER_NAME, PASSWORD, f"test user {ID}")
sign_in(USER_NAME, PASSWORD)
test_get_cv_file()
test_get_jobs()
test_upload_file()
test_get_cv_file()
test_get_avatar()
test_chatbot()
test_get_jobs()