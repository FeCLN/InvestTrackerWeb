from django.db import models
from django.contrib.auth.models import User

class StockData(models.Model):
    symbol = models.TextField(null=True)
    data = models.TextField(null=True)
