from socket import fromshare
from django import forms
from doubts.models import MyUser
from django.contrib.auth.forms import UserCreationForm
from doubts.models import Questions

class RegistrationForm(UserCreationForm):
    class Meta:
        model=MyUser
        fields=['first_name','last_name','username','email','phone','profile_pic','password1','password2']

class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={"class":"form-control border border-primary","placeholder":"enter username"}))
    password = forms.CharField(widget=forms.PasswordInput({"class":"form-control border border-primary","placeholder":"enter password"}))

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Questions
        fields = ["question","image"] 

        widgets = {
            "question":forms.Textarea(attrs={"class":"form-control","rows":3}),
            "image":forms.FileInput(attrs={"class":"form-select"})
        }