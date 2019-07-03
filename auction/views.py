from django.db.models import Q
from django.http import HttpRequest
from django.shortcuts import render, redirect

from auction.forms import AuctionForm
from django.http import Http404
from auction.models import Auction
from django.db import IntegrityError
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required


# Create your views here.
def home(request: HttpRequest):
    return render(
        request,
        template_name='home.html',
        context={}
    )


def auctions(request: HttpRequest):
    if 'search' in request.GET:
        search = request.GET['search'].lower()
        auctions = Auction.objects.filter(Q(lc_name__contains=search) | Q(lc_description__contains=search), started=1)
    else:
        search = ''
        auctions=Auction.objects.filter(started=1)

    items_per_page = 10
    paginator = Paginator(auctions, items_per_page)
    try:
        page = int(request.GET.get('page', 1))
    except ValueError:
        raise Http404

    if page not in paginator.page_range:
        raise Http404

    auctions = paginator.get_page(page)

    return render(
        request,
        template_name='auctions.html',
        context={
            'auctions': auctions,
            'paginator': paginator,
            'page': page,
            'search': search
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

    permissions = _auction_view_permissions(auction, request.user)

    return render(
        request,
        template_name='auction.html',
        context={
            'auction': auction,
            'parent_of_empty_comment': parent_of_empty_comment,
            'comment_save_called': comment_save_called,
            'active_tab': active_tab,
            'invalid_stake': invalid_stake,
            'permissions': permissions
        }
    )


def _auction_view_permissions(auction, user):
    winner = auction.winner()
    finished = auction.finished()

    permissions = dict()
    permissions['can_make_a_stake'] = (
        user.is_authenticated
        and auction.started
        and not finished
        and user.id != auction.user.id
    )
    permissions['can_edit'] = (
        user.is_authenticated
        and not auction.started
        and user.id == auction.user.id
    )
    permissions['can_delete'] = (
        user.is_authenticated
        and user.id == auction.user.id
    )
    permissions['can_see_winner_name'] = (
        winner
        and (not user.is_authenticated or user.is_authenticated and user.id != winner.id)
    )
    permissions['can_see_auction_ended_message'] = (
        finished
        and not permissions['can_see_winner_name']
    )
    permissions['can_see_winner_contact'] = (
        user.is_authenticated
        and winner
        and auction.user.id == user.id
    )
    permissions['can_see_you_win_message'] = (
        user.is_authenticated
        and winner
        and winner.id == user.id
    )

    return permissions


@login_required
def auction_edit(request: HttpRequest, auction_id: int):
    form_data = request.session.pop('auction_form_data', None)

    if auction_id == 0:
        form = AuctionForm(data=form_data)
        auction = None
    else:
        try:
            auction = Auction.objects.get(pk=auction_id)
        except Auction.DoesNotExist:
            raise Http404
        if auction.user.id != request.user.id or auction.started:
            return redirect('home')
        form = AuctionForm(data=form_data, instance=auction)

    form.is_valid()

    return render(
        request,
        template_name='auction_edit.html',
        context={
            'auction_id': auction_id,
            'auction': auction,
            'form': form
        }
    )


@login_required
def auction_save(request: HttpRequest, auction_id: int):
    if auction_id == 0:
        auction = Auction(user=request.user)
    else:
        try:
            auction = Auction.objects.get(pk=auction_id)
        except Auction.DoesNotExist:
            return redirect('auction_edit', auction_id=auction_id)
        if auction.user.id != request.user.id or auction.started:
            return redirect('home')

    form = AuctionForm(data=request.POST, instance=auction)
    if form.is_valid():
        auction = form.save()
        return redirect('auction', auction_id=auction.id)

    request.session['auction_form_data'] = request.POST
    return redirect('auction_edit', auction_id=auction_id)


@login_required
def auction_delete(request: HttpRequest, auction_id: int):
    try:
        auction = Auction.objects.get(pk=auction_id)
        if auction.user.id != request.user.id:
            return redirect('home')
        auction.delete()
    except Auction.DoesNotExist:
        pass

    return redirect('user_auctions', user_id=request.user.id)


@login_required
def make_bet(request: HttpRequest, auction_id: int):
    if 'stake' not in request.POST:
        return redirect('auction', auction_id=auction_id)
    try:
        auction = Auction.objects.get(pk=auction_id)
    except Auction.DoesNotExist:
        return redirect('auction', auction_id=auction_id)
    if auction.user.id == request.user.id:
        return redirect('home')
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
