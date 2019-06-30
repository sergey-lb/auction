from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Auction(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=400)
    description = models.TextField()
    start_price = models.IntegerField()
    blitz_price = models.IntegerField()
    end_date = models.DateTimeField()
    location_city = models.CharField(max_length=400)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='+')
    started = models.BooleanField()


class Bet(models.Model):
    id = models.AutoField(primary_key=True)
    date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='+')
    bet = models.IntegerField()
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name='bets')


class Image(models.Model):
    id = models.AutoField(primary_key=True)
    filename = models.CharField(max_length=255)
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name='images')
