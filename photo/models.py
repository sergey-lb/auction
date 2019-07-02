from django.db import models
from auction.models import Auction


# Create your models here.
class Photo(models.Model):
    id = models.AutoField(primary_key=True)
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name='photos')
    file = models.ImageField(upload_to="auction_photo")
