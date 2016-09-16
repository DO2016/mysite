from django.db import models
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse, resolve
from .models import Item, DerivedItem, Ingredient, LoginForm
from django.db.models import Count, Sum, Avg
from django.contrib.auth import authenticate, login

# Create your views here.

#def f(x,l=[]):
#    for i in range(x):
#        l.append(i*i)
#    print(l) 

def index(request):
    # f(3)
    # f(3,[3,2,1])
    # f(3)

    # https://docs.djangoproject.com/en/dev/topics/auth/default/
    # from django.contrib.auth.models import User
    # user = User.objects.create_user('john', 'lennon@thebeatles.com', '123')
    # user.last_name = 'Lennon'
    # user.save()

    # Get published items
    latest_list = DerivedItem.objects.get_list_via_filter()
    item_list = Item.objects.select_related().annotate(sum_ings_price = Sum('ings__price'))
    context = {'latest_list': latest_list, 'item_list' : item_list}
    return render(request, 'app2/index2.html', context)


def login_view(request):
    print '*********************'
    # Add if for POST in view and use LoginForm for getting and validate POST parameters.
    form = LoginForm(data=request.POST)
  
    if form.is_valid():
        print 'LoginForm.is_valid() = True'
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(username=username, password=password)

        print username
        print password
        print user

        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse(request.resolver_match.namespace + ':index', current_app = request.resolver_match.namespace))
    else:
        print form.errors.as_data()
    return render(request, 'app2/login.html')


def logout(request):
    from django.contrib.auth import logout
    logout(request)
    return HttpResponseRedirect(reverse(request.resolver_match.namespace + ':login', current_app = request.resolver_match.namespace))