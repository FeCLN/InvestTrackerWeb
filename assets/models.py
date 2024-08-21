from django.db import models
from django.contrib.auth.models import User

class Asset(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ticker = models.TextField(null=True)
    interval = models.IntegerField()
    upperLimit = models.DecimalField(decimal_places=2, max_digits=6)
    lowerLimit = models.DecimalField(decimal_places=2, max_digits=6)
