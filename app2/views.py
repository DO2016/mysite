from django.db import models
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse, resolve
from .models import Item, DerivedItem, Ingredient, LoginForm, CustomUser
from django.db.models import Count, Sum, Avg
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.template import Context, Template
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, UserManager

# Create your views here.

#def f(x,l=[]):
#    for i in range(x):
#        l.append(i*i)
#    print(l) 

@login_required(login_url='login.html')
def index(request):
    # f(3)
    # f(3,[3,2,1])
    # f(3)

    # https://docs.djangoproject.com/en/dev/topics/auth/default/
    # from django.contrib.auth.models import User
    # user = User.objects.create_user('john', 'lennon@thebeatles.com', '123')
    # user.last_name = 'Lennon'
    # user.save()

    # https://docs.djangoproject.com/en/dev/topics/auth/default/
    from django.contrib.auth.models import User
    user = CustomUser.objects.create_user('user', 'user@mail.com', '123')
    user.last_name = 'Lastname'
    user.save()

    # Get published items
    latest_list = DerivedItem.objects.get_list_via_filter()
    item_list = Item.objects.select_related().annotate(sum_ings_price = Sum('ings__price'))
    context = {'latest_list': latest_list, 'item_list' : item_list}
    return render(request, 'app2/index2.html', context)


def profile_view(request, pk=-1):
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


def login_view(request):
    context = Context({})
    # Add if for POST in view and use LoginForm for getting and validate POST parameters.
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        
        if form.is_valid():
            login(request, LoginForm.current_user)
            return redirect(reverse(request.resolver_match.namespace + ':index', current_app = request.resolver_match.namespace))
        else:
            print form.errors.as_data()
            context = Context({ 'form' : form })
            return render(request, 'app2/login.html', context)

    elif request.method == 'GET':
        context = Context({ 'market_title' : 'Welcome', 'form' : LoginForm })
    return render(request, 'app2/login.html', context)


def logout_view(request):
    logout(request)
    LoginForm.current_user = None
    return redirect(reverse(request.resolver_match.namespace + ':login_view', current_app = request.resolver_match.namespace))
