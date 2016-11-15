import uuid
import random
import string
import datetime
from dateutil import tz

from django.db import models
from django.views import View
from django.conf import settings
from django.utils import timezone
from django.shortcuts import render
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth import logout
from django.core.mail import send_mail
from django.db.models import Count, Sum, Avg
from django.views.generic import TemplateView
from django.template import Context, Template
from django.http import HttpResponseBadRequest
from django.views.generic.list import ListView
from django.views.generic.edit import FormView
from django.views.generic.base import RedirectView
from django.views.generic.detail import DetailView
from django.contrib.auth import authenticate, login
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User, UserManager
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse, reverse_lazy, resolve

from .forms import RegistrationForm, LoginForm
from .models import Product, Ingredient, CustomUser, Order


# Create your views here.

#class IndexView(RedirectView):
#    def get_redirect_url(self):
#        return reverse('showcase:products')


class IndexView(TemplateView):
    template_name = 'showcase/base.html'


class ProfileView(DetailView):
    model = CustomUser
    template_name='showcase/profile.html'
    context_object_name = 'object'


class RegistrationView(FormView):
    template_name = 'showcase/registration.html'
    form_class = RegistrationForm
    success_url = reverse_lazy('showcase:register')

    def _send_email(self, user):
        root_path = self.absolute_uri.split("/showcase", 1)
        content = root_path[0] + reverse("showcase:confirm", kwargs={'confirmation_code' : user.confirmation_code, 'username' : user.username})
        send_mail("Account confirmation", content, settings.EMAIL_HOST_USER, [user.email], fail_silently=False)

    def _create_new_user(self, username, last_name, email, password):
        # https://docs.djangoproject.com/en/dev/topics/auth/default/
        extra_fields = { 'last_name' : last_name, 'is_active' : False, 'confirmation_code' : str(uuid.uuid4()) }
        user = CustomUser.objects.create_user(username, email, password, **extra_fields)
        return user

    def post(self, request):
        form = RegistrationForm(data=request.POST)

        if form.is_valid():
            self.absolute_uri = request.build_absolute_uri()
            messages.info(request, 'Registration success!')
            messages.info(request, 'Look your email for confirmation letter!')
        return super(RegistrationView, self).post(request)

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        user = self._create_new_user(form.cleaned_data['first_name'] , form.cleaned_data['last_name'], form.cleaned_data['email'], form.cleaned_data['password'])
        self._send_email(user)
        return super(RegistrationView, self).form_invalid(form)


class ConfirmationView(TemplateView):
    template_name = "showcase/confirmation.html"

    def _check(self, request, **kwargs):
        ok = True
        user = None
        username = kwargs.get('username', '')
        confirmation_code = kwargs.get('confirmation_code', '')

        try:
            user = CustomUser.objects.get(username=username)
        except ObjectDoesNotExist:
            messages.error(request, 'User does not exists')
            ok = False
        else:
            if user.confirmation_code <> confirmation_code:
                messages.error(request, 'Confirmation code is invalid')
                ok = False
            else:              
                now = datetime.datetime.utcnow().replace(tzinfo=tz.gettz(user.timezone))

                if user.date_joined <= (now - datetime.timedelta(days=1)):
                    messages.error(request, 'Time is expired')
                    ok = False
                else:
                    user.is_active = True;
                    user.save();
        return ok

    def get(self, request, *args, **kwargs):
        if self._check(self, *args, **kwargs):
            return redirect(reverse('showcase:login'))
        return super(ConfirmationView, self).get(request, *args, **kwargs)
        

class LoginView(FormView):
    template_name = 'showcase/login.html'
    form_class = LoginForm
    success_url = reverse_lazy('showcase:index')

    def get(self, request):
        LoginView.success_url = request.GET.get('next', reverse_lazy('showcase:index'))
        return super(LoginView, self).get(request)

    def post(self, request):
        form = LoginForm(data=request.POST)

        if form.is_valid():
            if form.current_user.is_active:
                login(request, form.current_user)
            else:
                messages.error(request, 'Your account is not confirmed yet. Look your email for conformation letter!')
        else:
            messages.error(request, 'Error has been occured during login operation.')
        return super(LoginView, self).post(request)

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        if form.current_user.is_active == False:
            return super(LoginView, self).form_invalid(form)
        return super(LoginView, self).form_valid(form)


class LogoutView(RedirectView):
    def get(self, request):
        logout(request)
        return super(LogoutView, self).get(request)

    def get_redirect_url(self):
        return reverse('showcase:login')


class ProductDetail(DetailView):
    model = Product
    template_name='showcase/product_detail.html'
    context_object_name = 'object'


class ProductListView(ListView):
    model = Product
    paginate_by = 2
    context_object_name = 'product_list'
    template_name = 'showcase/product_list.html'

    def dispatch(self, request, *args, **kwargs):
        return super(ProductListView, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return Product.objects.all_published()

