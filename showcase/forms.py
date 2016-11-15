from django import forms
from django.conf import settings
from django.contrib.auth import authenticate
from django.http import HttpResponse, HttpResponseRedirect

from .models import Product, Ingredient, CustomUser


class LoginForm(forms.Form):
    username = forms.CharField(max_length=256, required=True)
    password = forms.CharField(widget=forms.PasswordInput(), max_length=256, required=True)

    def __unicode__(self):
        return 'Login form'

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

        if len(password) < settings.USER_PSW_MIN_LENGTH:
            raise forms.ValidationError("Password length should be at least " + str(LoginForm._pass_min_length))
        else:
            self._current_user = authenticate(username=username, password=password)

            if self._current_user is None:
                raise forms.ValidationError("User authentication failed !!")

        # Always return the cleaned data, whether you have changed it or not.
        return password


class RegistrationForm(forms.Form):
    first_name = forms.CharField(max_length=256, required=True)
    last_name = forms.CharField(max_length=256, required=True)
    password = forms.CharField(widget=forms.PasswordInput(), max_length=256, required=True)
    email = forms.CharField(max_length=256, required=True)

    def __unicode__(self):
        return 'Registration form'

    class Meta:
        fields = ('first_name', 'last_name', 'password', 'email')

    def clean_password(self):
        password = self.cleaned_data['password']

        if len(password) < settings.USER_PSW_MIN_LENGTH:
            print 'Password length validation failure.'
            raise forms.ValidationError("Password length should be at least " + str(settings.USER_PSW_MIN_LENGTH))
        return password



class UserModelMultipleChoiceField(forms.ModelMultipleChoiceField):
    def label_from_instance(self, obj):
        return super(UserModelMultipleChoiceField, self).label_from_instance(obj)


class IngredientAdminForm(forms.ModelForm):
    products = UserModelMultipleChoiceField(queryset=Product.objects.all_published())
    class Meta:
        model = Ingredient
        fields = '__all__'

