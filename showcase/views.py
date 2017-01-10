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

class IndexView(TemplateView):
    template_name = 'showcase/base.html'
