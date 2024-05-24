from django.urls import include, path
from . import views

user_urls = [
  path('cv/', views.UserCVView.as_view()),
  path('avatar/', views.UserAvatarView.as_view()),
]

api_urls = [
  path('signup/', views.SignUpView.as_view()),
  path('signin/', views.SignInView.as_view()),
  path('forgot-password/', views.ForgotPasswordView.as_view()),
  path('user/', include(user_urls)),
  path('jobs/', views.JobView.as_view()),
  path('chatbot/', views.ChatBotView.as_view()),
]
