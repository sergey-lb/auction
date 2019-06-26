from django.http import HttpRequest
from django.shortcuts import render


# Create your views here.
def home(request: HttpRequest):
    return render(
        request,
        template_name='home.html',
        context={}
    )


def auctions(request: HttpRequest):
    return render(
        request,
        template_name='auctions.html',
        context={}
    )


def auction(request: HttpRequest, auction_id: int):
    return render(
        request,
        template_name='auction.html',
        context={}
    )


def auction_edit(request: HttpRequest, auction_id: int):
    return render(
        request,
        template_name='auction_edit.html',
        context={}
    )


def auction_save(request: HttpRequest, auction_id: int):
    return None


def auction_delete(request: HttpRequest, auction_id: int):
    return None
