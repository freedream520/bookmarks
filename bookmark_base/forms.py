from django import forms
import re
from django.contrib.auth.models import User

class RegisteForm(forms.Form):
    username=forms.CharField(label=u'Username',max_length=30)
    email=forms.EmailField(label=u'Email')
    password1=forms.CharField(
        label=u'Password',
        widget=forms.PasswordInput()
        )
    password2=forms.CharField(
        label=u'Password Again',
        widget=forms.PasswordInput()
        )
    def clearpassword2(self):
        if 'password1' in self.cleaned_data:
            password1=self.cleaned_data['password1']
            password2=self.cleaned_data['password2']
            if password1 == password2:
                return password2
        raise forms.ValidationError('Passwords not match')
    def clearusername(self):
        username=self.cleaned_data['username']
        if not re.search(r'^\w+$',username):
            raise forms.ValidationError("username can't contains not alpha or number")
        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError('username already exits')

class BookmarkForm(forms.Form):
    url=forms.URLField(
        label=u'URL',
        widget=forms.TextInput(attrs={'size':100})
        )
    title=forms.CharField(
        label=u'Title',
        widget=forms.TextInput(attrs={'size':100})
        )
    tag=forms.CharField(
        label=u'Tag',
        required=False,
        widget=forms.TextInput(attrs={'size':100})
        )
    share=forms.BooleanField(
        label=u'share on the main page',
        required=False
        )

class SearchForm(forms.Form):
    query=forms.CharField(
        label=u'',
        widget=forms.TextInput(attrs={'size':36})
        )    
