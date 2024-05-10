from django import forms

class SignUpForm(forms.Form):
  email = forms.EmailField()
  password = forms.CharField()
  username = forms.CharField()

class SignInForm(forms.Form):
  email = forms.EmailField()
  password = forms.CharField()

class ForgotPasswordForm(forms.Form):
  email = forms.EmailField()