from django.db import models

class Truck(models.Model):
    name = models.CharField(max_length=30)

    def __unicode__(self):
        return self.name

class Event(models.Model):
    id = models.BigIntegerField(primary_key=True)
    date = models.DateField()
    trucks = models.ManyToManyField(Truck)

    def __unicode__(self):
        return u'%s %s' % (self.id, self.date)

