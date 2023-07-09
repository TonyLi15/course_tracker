from django import forms
from django.contrib.auth.models import User
from .models import *

class AccountForm(forms.ModelForm):
    # When typing password, it is not shown
    password = forms.CharField(widget=forms.PasswordInput(),label="Password")
    
    class Meta():
        model = User
        fields = ('username','email','password')
        labels = {'username':"User ID",'email':"Email"}

class AddAccountForm(forms.ModelForm):
    class Meta():
        model = Account
        fields = ('last_name','first_name')
        labels = {'last_name':"Last Name",'first_name':"First Name",}

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['title','credit','faculty','professor','intro',]
        labels = {'title':"Title",'credit':"credit",'faculty':"faculty",'professor':"Professor",'intro':"Introduction",}

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["body", "score"]

class ScoreForm(forms.ModelForm):
    score = forms.ChoiceField(choices=Comment.SCORE_CHOICES, widget=forms.RadioSelect(attrs={'class': 'horizontal-radio'}))