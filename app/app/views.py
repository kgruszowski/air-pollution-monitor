from django.shortcuts import render
from .model import Stations, Monitoring

def index(request):

    stations = Stations.getStationAndStatus(Stations)

    context = {
        'stations': stations
    }

    return render(request, 'index.html', context)

def stationDetails(request, station_id):

    station = Stations.objects.get(id=station_id)
    monitoring = station.monitoring_set.all().order_by('date').reverse()

    monitoringCharts = monitoring.reverse()

    context = {
        'station': station,
        'monitoring': monitoring,
        'charts': monitoringCharts
    }

    return render(request, 'station_details.html', context)
