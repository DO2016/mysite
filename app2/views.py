from django.db import models
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse, resolve
from .models import Item, DerivedItem, Ingredient
from django.db.models import Count, Sum, Avg

# Create your views here.

def f(x,l=[]):
    for i in range(x):
        l.append(i*i)
    print(l) 

def index(request):
    f(3)
    # f(3,[3,2,1])
    f(3)

    # Get published items
    latest_list = DerivedItem.objects.get_list_via_filter()
    item_list = Item.objects.select_related().annotate(sum_ings_price = Sum('ings__price'))
    context = {'latest_list': latest_list, 'item_list' : item_list}
    return render(request, 'app2/index2.html', context)
    #return HttpResponse(reverse(request.resolver_match.namespace + ':index', current_app = request.resolver_match.namespace))