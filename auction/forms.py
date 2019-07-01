from django.forms import ModelForm
from auction.models import Auction


class AuctionForm(ModelForm):
    class Meta:
        model = Auction
        fields = ['name', 'description', 'start_price', 'blitz_price', 'end_date', 'started', 'location_city']
