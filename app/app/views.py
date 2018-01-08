from django.shortcuts import render
# from .model import Stations, Monitoring

def index(request):

    # stations = Stations.objects.all()

    context = {
        'stations': {}
    }

    return render(request, 'index.html', context)