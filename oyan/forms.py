from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from catalog.models import Articles

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Articles
        fields = ['title', 'description', 'content', 'release']

        widgets = {
            'title': forms.TextInput(attrs={'class': 'title-class'}),
            'description': forms.Textarea(attrs={'class': 'content-class'}),
            'content': forms.Textarea(attrs={
                'class': 'content-class',
                 "minlength": 100, 
                 "maxlength": 2000
            }),
            "release": forms.DateInput(attrs={
                "type": "date",
                'class': 'release-class',
                })
        }



class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
