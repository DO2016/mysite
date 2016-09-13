from django.db import models
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse, resolve
from .models import Item, DerivedItem
from django.db.models import Count, Sum, Avg

# Create your views here.

def index(request):
    # Get published items
    latest_list = DerivedItem.objects.get_list_via_filter()
    item_list = Item.objects.select_related()

    context = {'latest_list': latest_list, 'item_list' : item_list}
    return render(request, 'app2/index2.html', context)
    #return HttpResponse(reverse(request.resolver_match.namespace + ':index', current_app = request.resolver_match.namespace))