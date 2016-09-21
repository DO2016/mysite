from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import ModelTable, Post, PostForm, BookForm
from django.core.urlresolvers import reverse, resolve


def index(request):
    latest_list = ModelTable.objects.order_by('-col1')[:5]
    context = {'latest_list': latest_list}
    return HttpResponseRedirect(reverse(request.resolver_match.namespace + ':index_table', current_app = request.resolver_match.namespace))
    #return HttpResponseRedirect(reverse('index_table'))
    #return render(request, 'app1/index.html', context)


def index_table(request):
    latest_list = ModelTable.objects.order_by('-col1')[:5]
    context = {'latest_list': latest_list}
    return render(request, 'app1/index2.html', context)

#def index(request):
#    latest_list = ModelTable.objects.order_by('-col1')[:5]
#    template = loader.get_template('app1/index.html')
#    context = RequestContext(request, {
#        'latest_question_list': latest_list,
#    })
#    return HttpResponse(template.render(context))

#def index(request):
#    return HttpResponse("Hello, world. You're at the app1 index.")

def article_detail(request, **kwargs):
    year = kwargs.get('year', -1)
    month = kwargs.get('month', -1)
    day = kwargs.get('day', -1)

    if int(year) > 0 and int(month) > 0 and int(day) > 0:
        return HttpResponse("Your choice: " + " ".join([year, month, day]))
    return HttpResponse("Error : Data is not valid.")


def month_archive(request, year, month):
    return HttpResponse("Your choice: " + request.path + "  " + " ".join([year, month]))


def post_view(request):
    context = { 'form': BookForm() }
    return render(request, 'app1/post.html', context)

	