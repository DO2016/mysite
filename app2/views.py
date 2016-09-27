import random
import string
import pytz, datetime
from django.db import models
from django.views import View
from django.conf import settings
from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth import logout
from django.core.mail import send_mail
from django.db.models import Count, Sum, Avg
from django.template import Context, Template
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.contrib.auth import authenticate, login
from django.core.urlresolvers import reverse, resolve
from django.contrib.auth.models import User, UserManager
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from .models import Item, DerivedItem, Ingredient, LoginForm, RegistrationForm, CustomUser

# Create your views here.

#class MyView(View):
#    def get(self, request):
#        # <view logic>
#        return HttpResponse('result')


class IndexView(View):
    #@login_required(login_url='login.html')
    def get(self, request):
        # Get published items
        latest_list = DerivedItem.objects.get_list_via_filter()
        item_list = Item.objects.select_related().annotate(sum_ings_price = Sum('ings__price'))
        context = {'latest_list': latest_list, 'item_list' : item_list}
        return render(request, 'app2/index2.html', context)


class ProfileView(View):
    def get(self, request, pk=-1):
        if (pk > -1):
            user_pk_int = int(pk)
        else:
            user_pk_int = int(request.GET.get('pk', '0'))
            pk = user_pk_int
        try:
            user = User.objects.get(id=user_pk_int)
        except:
            context = Context({ 'user_pk' : pk, 'user_name' : 'Not found', 'user_email' : 'Not found' })      
        else:
            context = Context({ 'user_pk' : pk, 'user_name' : user.username, 'user_email' : user.email })
        return render(request, 'app2/profile.html', context)


class RegistrationView(View):
    def _send_email(self, user):
        content = "127.0.0.1:8080/app2/confirm/" + str(user.confirmation_code) + "/" + user.username
        send_mail("Account confirmation", content, settings.EMAIL_HOST_USER, [user.email], fail_silently=False)


    def _create_new_user(self, username, last_name, email, password):
        # https://docs.djangoproject.com/en/dev/topics/auth/default/
        user = CustomUser.objects.create_user(username, email, password)
        user.last_name = last_name
        user.is_active = False
        user.confirmation_code = ''.join(random.choice(string.ascii_uppercase + string.digits + string.ascii_lowercase) for x in range(33))
        user.save()
        return user

    def get(self, request):
        context = Context({ 'market_title' : 'New account registration page', 'form' : RegistrationForm })
        return render(request, 'app2/registration.html', context)

    def post(self, request):
        context = Context({})
        form = RegistrationForm(data=request.POST)
        
        if form.is_valid():
            user = self._create_new_user(form.cleaned_data['first_name'] , form.cleaned_data['last_name'], form.cleaned_data['email'], form.cleaned_data['password'])
            self._send_email(user)
            context = Context({ 'market_title' : 'Registration success!', 'reg_complete_msg' : 'Look your email for conformation letter!',  'form' : RegistrationForm })
            return render(request, 'app2/registration.html', context)
        else:
            print form.errors.as_data()
            context = Context({ 'form' : form })
            return render(request, 'app2/registration.html', context)



class ConfirmationView(View):
    def get(self, request, confirmation_code, username):
        user = CustomUser.objects.get(username=username)
        tz = pytz.timezone(user.timezone)

        if user.confirmation_code == confirmation_code and user.date_joined > (datetime.datetime.now(tz) - datetime.timedelta(days=1)):
            user.is_active = True
            user.save()
            #user.backend='django.contrib.auth.backends.ModelBackend' 
        return redirect('LoginView.as_view()')
        #return redirect(reverse(request.resolver_match.namespace + ':login_view', current_app = request.resolver_match.namespace))


class LoginView(View):
    def post(self, request):
        context = Context({})
        form = LoginForm(data=request.POST)

        if form.is_valid():
            if form.current_user.is_active:
                login(request, form.current_user)
                return redirect(reverse(request.resolver_match.namespace + ':index', current_app = request.resolver_match.namespace))
            else:
                context = Context({ 'market_title' : 'Your account is not confirmed yet!', 'reg_complete_msg' : 'Look your email for conformation letter!', 'form' : RegistrationForm })
                return render(request, 'app2/registration.html', context)
        else:
            print form.errors.as_data()
            context = Context({ 'form' : form, 'market_title' : 'Failed: ' + LoginForm.current_password })
            return render(request, 'app2/login.html', context)
        return render(request, 'app2/login.html', context)

    def get(self, request):
        context = Context({ 'market_title' : 'Welcome', 'form' : LoginForm })
        return render(request, 'app2/login.html', context)


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect(reverse(request.resolver_match.namespace + ':login_view', current_app = request.resolver_match.namespace))


class ItemListView(ListView):
    model = Item
    paginate_by = 10
    context_object_name = 'latest_list'
    template_name = 'app2/item_list.html'

    #@method_decorator(login_required)
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

