from django import forms
from helloworld.models import Helloworld
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model


class SnippetForm(forms.ModelForm):
    class Meta:
        model = Helloworld
        fields = ('title', 'code', 'description')


User = get_user_model()
class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'school_year')