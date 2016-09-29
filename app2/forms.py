
from django import forms
from django.contrib.auth import authenticate
from django.http import HttpResponse, HttpResponseRedirect
from .models import Item, DerivedItem, Ingredient, CustomUser

class LoginForm(forms.Form):
    username = forms.CharField(max_length=256, required=True)
    password = forms.CharField(widget=forms.PasswordInput(), max_length=256, required=True)
    _pass_min_length = 3
    current_password = None

    class Meta:
        fields = ('username', 'password')

    @property
    def current_user(self):
        return self._current_user

    @current_user.setter
    def current_user(self, value):
        self._current_user = value

    def clean_password(self):
        password = self.cleaned_data['password']
        username = self.cleaned_data['username']
        self._current_user = None

        if len(password) < LoginForm._pass_min_length:
            print 'Password length validation failure.'
            raise forms.ValidationError("Password length should be at least " + str(LoginForm._pass_min_length))
        else:
            self._current_user = authenticate(username=username, password=password)

            if self._current_user is None:
                LoginForm.current_password = username + ' / ' + password
                raise forms.ValidationError("User authentication failed !!")

        # Always return the cleaned data, whether you have changed it or not.
        return password


class RegistrationForm(forms.Form):
    first_name = forms.CharField(max_length=256, required=True)
    last_name = forms.CharField(max_length=256, required=True)
    password = forms.CharField(widget=forms.PasswordInput(), max_length=256, required=True)
    email = forms.CharField(max_length=256, required=True)
    _pass_min_length = 3

    class Meta:
        fields = ('first_name', 'last_name', 'password', 'email')

    def clean_password(self):
        password = self.cleaned_data['password']

        if len(password) < RegistrationForm._pass_min_length:
            print 'Password length validation failure.'
            raise forms.ValidationError("Password length should be at least " + str(LoginForm._pass_min_length))
        return password