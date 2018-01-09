from django.shortcuts import render
from .model import Stations, Monitoring

def index(request):

    stations = Stations.getStationAndStatus(Stations)

    context = {
        'stations': stations
    }

    return render(request, 'index.html', context)