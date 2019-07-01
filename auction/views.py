from django.db.models import Q
from django.http import HttpRequest
from django.shortcuts import render, redirect

from auction.forms import AuctionForm
from django.http import Http404
from auction.models import Auction
from django.db import IntegrityError


# Create your views here.
def home(request: HttpRequest):
    return render(
        request,
        template_name='home.html',
        context={}
    )


def auctions(request: HttpRequest):
    if 'search' in request.GET:
        search = request.GET['search']
        auctions = Auction.objects.filter(Q(name__contains=search) | Q(description__contains=search))
    else:
        auctions=[]

    return render(
        request,
        template_name='auctions.html',
        context={
            'auctions': auctions
        }
    )


def user_auctions(request: HttpRequest, user_id: int):
    auctions = Auction.objects.filter(user_id=user_id)
    return render(
        request,
        template_name='auctions.html',
        context={
            'auctions': auctions
        }
    )


def auction(request: HttpRequest, auction_id: int):
    try:
        auction = Auction.objects.get(pk=auction_id)
    except Auction.DoesNotExist:
        raise Http404

    parent_of_empty_comment = request.session.pop('parent_of_empty_comment', None)
    comment_save_called = request.session.pop('comment_save_called', None)
    bet_saved = request.session.pop('bet_saved', None)
    invalid_stake = request.session.pop('invalid_stake', None)

    active_tab = 'description'
    if comment_save_called:
        active_tab = 'q-and-a'
    elif bet_saved:
        active_tab = 'stakes'

    return render(
        request,
        template_name='auction.html',
        context={
            'auction': auction,
            'parent_of_empty_comment': parent_of_empty_comment,
            'comment_save_called': comment_save_called,
            'active_tab': active_tab,
            'invalid_stake': invalid_stake
        }
    )


def auction_edit(request: HttpRequest, auction_id: int):
    form_data = request.session.pop('auction_form_data', None)

    if auction_id == 0:
        form = AuctionForm(data=form_data)
    else:
        try:
            auction = Auction.objects.get(pk=auction_id)
        except Auction.DoesNotExist:
            raise Http404
        form = AuctionForm(data=form_data, instance=auction)

    form.is_valid()

    return render(
        request,
        template_name='auction_edit.html',
        context={
            'auction_id': auction_id,
            'form': form
        }
    )


def auction_save(request: HttpRequest, auction_id: int):
    if auction_id == 0:
        auction = Auction(user=request.user)
    else:
        try:
            auction = Auction.objects.get(pk=auction_id)
        except Auction.DoesNotExist:
            return redirect('auction_edit', auction_id=auction_id)

    form = AuctionForm(data=request.POST, instance=auction)
    if form.is_valid():
        auction = form.save()
        return redirect('auction', auction_id=auction.id)

    request.session['auction_form_data'] = request.POST
    return redirect('auction_edit', auction_id=auction_id)


def auction_delete(request: HttpRequest, auction_id: int):
    try:
        auction = Auction.objects.get(pk=auction_id)
        auction.delete()
    except Auction.DoesNotExist:
        pass

    return redirect('user_auctions', user_id=request.user.id)


def make_bet(request: HttpRequest, auction_id: int):
    if 'stake' not in request.POST:
        return redirect('auction', auction_id=auction_id)

    try:
        auction = Auction.objects.get(pk=auction_id)
    except Auction.DoesNotExist:
        return redirect('auction', auction_id=auction_id)

    try:
        stake = int(request.POST['stake'])
    except ValueError:
        stake = 0

    if stake < auction.start_price:
        request.session['invalid_stake'] = stake
        return redirect('auction', auction_id=auction_id)

    try:
        auction.bets.create(
            user_id=request.user.id,
            bet=stake
        )
        request.session['bet_saved'] = True
    except IntegrityError:
        pass

    return redirect('auction', auction_id=auction_id)
