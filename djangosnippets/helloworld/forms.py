from django import forms
from helloworld.models import Helloworld, Lecture, Review
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
#from helloworld.models import Manager

class SnippetForm(forms.ModelForm):
    class Meta:
        model = Helloworld
        fields = ('title', 'code', 'description')


User = get_user_model()
#ユーザ登録
class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'school_year', 'university')

#ユーザ編集
class CustomUserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'school_year', 'university']


class ManagerForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username','email')
    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            User.objects.create(user=user)
        return user


class LectureForm(forms.ModelForm):
    class Meta:
        model = Lecture
        fields = ('name', 'body', 'university', 'school_year')


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ('title', 'comment', 'score')

