from django.shortcuts import render
from django.http import HttpResponse
from pages.models import Page
# Create your views here.

def Background(request):
    # query the database to return all project objects
    pages = Page.objects.filter(topic__iexact='background').order_by('id')
    return render(request, 'pages/page.html',
                  {'pages': pages})

def Pages(request, topic):
        # query the database to return all project objects
        pages = Page.objects.filter(topic__iexact=topic).order_by('id')
        return render(request, 'pages/page.html',
                      {'pages': pages})


