from django.shortcuts import render
from django.http import HttpResponse
from dashboard.models import Graph


# Create your views here.

def all_graphs(request):
    # query the database to return all project objects
    graphs = Graph.objects.all()
    return render(request, 'dashboard/graph.html',
                  {'graphs': graphs})


def section_graphs(request, topic):
    # query the database to return all project objects
    graphs = Graph.objects.filter(topic__iexact=topic)
    return render(request, 'dashboard/graph.html',
                  {'graphs': graphs})




