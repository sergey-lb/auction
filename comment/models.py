from django.db import models
from django.contrib.auth.models import User
from auction.models import Auction


# Create your models here.
class Comment(models.Model):
    id = models.AutoField(primary_key=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, related_name='comments')
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='+')
    date = models.DateTimeField(auto_now_add=True)
    comment = models.TextField()
