from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse, resolve
from .models import Item

# Create your views here.

def index(request):
    # Get published items
    latest_list = Item.objects.get_list_via_filter()
    context = {'latest_list': latest_list}
    return render(request, 'app2/index2.html', context)
    #return HttpResponse(reverse(request.resolver_match.namespace + ':index', current_app = request.resolver_match.namespace))