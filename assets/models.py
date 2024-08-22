from django.db import models
from django.contrib.auth.models import User

class Asset(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ticker = models.TextField(null=True)
    interval = models.IntegerField()
    upperLimit = models.DecimalField(decimal_places=2, max_digits=6)
    lowerLimit = models.DecimalField(decimal_places=2, max_digits=6)
    tunnelType = models.TextField(null=True) #static; async; sync


class AssetHistory(models.Model):
    asset      = models.ForeignKey(Asset, on_delete=models.CASCADE)
    timestamp  = models.TextField(null=True)
    openPrice  = models.DecimalField(decimal_places=2, max_digits=6)
    highPrice  = models.DecimalField(decimal_places=2, max_digits=6)
    lowPrice   = models.DecimalField(decimal_places=2, max_digits=6)
    closePrice = models.DecimalField(decimal_places=2, max_digits=6)


