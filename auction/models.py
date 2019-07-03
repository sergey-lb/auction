from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
import pytz


# Create your models here.
class Auction(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=400)
    lc_name = models.CharField(max_length=400)
    description = models.TextField()
    lc_description = models.TextField()
    start_price = models.IntegerField()
    blitz_price = models.IntegerField()
    end_date = models.DateTimeField()
    location_city = models.CharField(max_length=400)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='+')
    started = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        self.lc_name = self.name.lower()
        self.lc_description = self.description.lower()
        super().save(*args, **kwargs)

    def max_bet(self):
        bets = self.bets.order_by('-bet')[:1]
        if bets:
            return bets[0].bet

        return 0

    def first_level_comments(self):
        comments = self.comments.filter(parent_id__isnull=True)
        return comments

    def finished(self):
        if self.max_bet() >= self.blitz_price:
            return True
        end_date = self.end_date
        now = pytz.utc.localize(datetime.now())
        if end_date <= now:
            return True
        return False

    def winner(self):
        if not self.finished():
            return None
        max_bet = self.bets.order_by('-bet')[:1]
        if not max_bet:
            return None
        winner = max_bet.user
        return winner


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
