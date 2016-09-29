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
from django.shortcuts import redirect
from django.contrib.auth import logout
from django.core.mail import send_mail
from django.db.models import Count, Sum, Avg
from django.views.generic import TemplateView
from django.template import Context, Template
from django.http import HttpResponseBadRequest
from django.views.generic.list import ListView
from .forms import RegistrationForm, LoginForm
from django.views.generic.edit import FormView
from django.views.generic.base import RedirectView
from django.views.generic.detail import DetailView
from django.contrib.auth import authenticate, login
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User, UserManager
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from .models import Item, DerivedItem, Ingredient, CustomUser
from django.core.urlresolvers import reverse, reverse_lazy, resolve



# Create your views here.

class IndexView(TemplateView):
    template_name = "app2/index2.html"

    def get_context_data(self, *args, **kwargs):
        context = super(IndexView, self).get_context_data(*args, **kwargs)
        item_list = Item.objects.select_related().annotate(sum_ings_price = Sum('ings__price'))
        context['item_list'] = item_list
        return context


class ProfileView(DetailView):
    model = CustomUser
    template_name='app2/profile.html'
    context_object_name = 'object'

    def get_object(self):
        object = super(ProfileView, self).get_object()
        return object


class RegistrationView(FormView):
    template_name = 'app2/registration.html'
    form_class = RegistrationForm
    success_url = reverse_lazy('app2_nms1:register')

    market_title = ''
    reg_complete_msg = ''

    @classmethod
    def init_class_vars(cls):
        cls.market_title = 'New account registration page'
        cls.reg_complete_msg = ''

    def _send_email(self, user):
        content = reverse("app2_nms1:confirm", kwargs={'confirmation_code' : user.confirmation_code, 'username' : user.username })
        #content = "127.0.0.1:8080/app2/confirm/" + str(user.confirmation_code) + "/" + user.username
        send_mail("Account confirmation", content, settings.EMAIL_HOST_USER, [user.email], fail_silently=False)

    def _create_new_user(self, username, last_name, email, password):
        # https://docs.djangoproject.com/en/dev/topics/auth/default/
        extra_fields = { 'last_name' : last_name, 'is_active' : False, 'confirmation_code' : str(uuid.uuid4()) }
        user = CustomUser.objects.create_user(username, email, password, **extra_fields)
        return user

    def get_context_data(self, **kwargs):
        context = super(RegistrationView, self).get_context_data(**kwargs)
        context['market_title'] = self.__class__.market_title
        context['reg_complete_msg'] = self.__class__.reg_complete_msg
        self.__class__.init_class_vars()
        return context

    def form_invalid(self, form):
        return super(RegistrationView, self).form_invalid(form)

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        user = self._create_new_user(form.cleaned_data['first_name'] , form.cleaned_data['last_name'], form.cleaned_data['email'], form.cleaned_data['password'])
        self._send_email(user)
        self.__class__.market_title = 'Registration success!'
        self.__class__.reg_complete_msg = 'Look your email for confirmation letter!'
        return super(RegistrationView, self).form_invalid(form)


class ConfirmationView(TemplateView):
    template_name = "app2/confirmation.html"

    def _check(self, *args, **kwargs):
        self.err = ''
        user = None
        username = kwargs.get('username', '')
        confirmation_code = kwargs.get('confirmation_code', '')

        try:
            user = CustomUser.objects.get(username=username)
        except ObjectDoesNotExist:
            self.err =  'User does not exists'
        else:
            if user.confirmation_code <> confirmation_code:
                self.err = 'Confirmation code is invalid'
            else:              
                now = datetime.datetime.utcnow().replace(tzinfo=tz.gettz(user.timezone))

                if user.date_joined <= (now - datetime.timedelta(days=1)):
                    self.err = 'Time is expired'
                else:
                    user.is_active = True;
                    user.save();

    def get(self, request, *args, **kwargs):
        self._check(self, *args, **kwargs)
        if not self.err:
            return redirect(reverse('app2_nms1:login'))
        return super(ConfirmationView, self).get(request, *args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super(ConfirmationView, self).get_context_data(*args, **kwargs)
        context['error_msg'] = self.err
        return context


class LoginView(FormView):
    template_name = 'app2/login.html'
    form_class = LoginForm
    success_url = reverse_lazy('app2_nms1:index')

    market_title = ''
    log_msg = ''

    @classmethod
    def init_class_vars(cls):
        cls.market_title = 'Welcome!'
        cls.log_msg = ''

    def get(self, request):
        self.__class__.success_url = request.GET.get('next', reverse_lazy('app2_nms1:index'))
        return super(LoginView, self).get(request)

    def post(self, request):
        form = LoginForm(data=request.POST)

        if form.is_valid():
            if form.current_user.is_active:
                login(request, form.current_user)
        return super(LoginView, self).post(request)

    def get_context_data(self, **kwargs):
        context = super(LoginView, self).get_context_data(**kwargs)
        context['market_title'] = self.__class__.market_title
        context['log_msg'] = self.__class__.log_msg
        self.__class__.init_class_vars()
        return context

    def form_invalid(self, form):
        kwargs = self.get_form_kwargs()
        self.__class__.market_title = 'Login error'
        self.__class__.log_msg = 'Error has been occured during login operation'
        return super(LoginView, self).form_invalid(form)

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        if form.current_user.is_active == False:
            self.__class__.market_title = 'Your account is not confirmed yet!'
            self.__class__.log_msg = 'Look your email for conformation letter!'
            return super(LoginView, self).form_invalid(form)
        return super(LoginView, self).form_valid(form)


class LogoutView(RedirectView):
    def get(self, request):
        logout(request)
        return super(LogoutView, self).get(request)

    def get_redirect_url(self):
        return reverse('app2_nms1:login')


class ItemListView(ListView):
    model = Item
    paginate_by = 10
    context_object_name = 'latest_list'
    template_name = 'app2/item_list.html'

    def dispatch(self, request, *args, **kwargs):
        return super(ItemListView, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return Item.objects.all()


class ItemDetail(DetailView):
    model = Item

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(ItemDetail, self).get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['item_list'] = Item.objects.all()
        return context

