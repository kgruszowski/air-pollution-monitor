# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models, connection


class Monitoring(models.Model):
    id = models.AutoField(primary_key=True)
    station = models.ForeignKey('Stations', models.DO_NOTHING, db_column='stationid', blank=True, null=True)
    pm2_5 = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    pm10 = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    temp = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'monitoring'


class Stations(models.Model):
    id = models.AutoField(primary_key=True)
    vendor = models.CharField(max_length=5, blank=True, null=True)
    stationid = models.IntegerField(blank=True, null=True)
    stationname = models.CharField(max_length=200, blank=True, null=True)
    lng = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    lat = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    city = models.CharField(max_length=20, blank=True, null=True)
    street = models.CharField(max_length=60, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'stations'

    def dictfetchall(cursor):
        columns = [col[0] for col in cursor.description]
        return [
            dict(zip(columns, row))
            for row in cursor.fetchall()
        ]

    def getStationAndStatus(self):
        with connection.cursor() as cursor:
            cursor.execute('SELECT s.*, m1.* '
                           'FROM stations s '
                           'JOIN monitoring m1 ON s.id = m1.stationid '
                           'LEFT OUTER JOIN monitoring m2 ON s.id = m2.stationid AND (m1.date < m2.date OR m1.date = m2.date AND m1.id < m2.id) '
                           'WHERE m2.id IS NULL;')
            rows = self.dictfetchall(cursor)

        return rows

