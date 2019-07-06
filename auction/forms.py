from django.core.exceptions import ValidationError
from django.forms import ModelForm
from auction.models import Auction
from datetime import datetime
from pytz import timezone
from AuctionApp import settings


class AuctionForm(ModelForm):
    class Meta:
        model = Auction
        fields = ['name', 'description', 'start_price', 'blitz_price', 'end_date', 'started', 'location_city']

    def __init__(self, *args, **kwargs):
        super(AuctionForm, self).__init__(*args, **kwargs)
        self.fields['end_date'].validators.append(
            self._end_date_validator
        )

    def _end_date_validator(self, value):
        tz = timezone(settings.TIME_ZONE)
        now = tz.localize(datetime.now())
        if value < now:
            raise ValidationError(
                'Дата окончания не может быть меньше текущей даты'
            )
