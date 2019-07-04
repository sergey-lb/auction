from django.http import HttpRequest
from django.http import JsonResponse
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt
from photo.forms import PhotoForm
from django.db import IntegrityError
from photo.models import Photo
from auction.models import Auction
from django.contrib.auth.decorators import login_required


# Create your views here.
@csrf_exempt
def photo_save(request: HttpRequest, auction_id: int):
    if not request.user.is_authenticated:
        return JsonResponse({'result': 0, 'msg': 'Вы не авторизованы'})
    try:
        auction = Auction.objects.get(pk=auction_id)
    except Auction.DoesNotExist:
        return JsonResponse({'result': 0, 'msg': 'Аукцион не существует'})
    if auction.user.id != request.user.id:
        return JsonResponse({'result': 0, 'msg': 'Ошибка загрузки файла'})

    photo = Photo(auction_id=auction_id)
    form = PhotoForm(request.POST, request.FILES, instance=photo)
    if form.is_valid():
        try:
            form.save()
        except IntegrityError:
            return JsonResponse({'result': 0, 'msg': 'Ошибка загрузки файла'})
    else:
        return JsonResponse({'result': 0, 'msg': 'Ошибка загрузки файла'})
    request.session['open_gallery_tab'] = True
    return JsonResponse({'result': 1})


@login_required
def photo_delete(request: HttpRequest, auction_id: int, photo_id: int):
    try:
        photo = Photo.objects.get(pk=photo_id)
        if photo.auction.user.id != request.user.id:
            return redirect('home')
        photo.delete()
    except Photo.DoesNotExist:
        pass
    request.session['open_gallery_tab'] = True
    return redirect('auction_edit', auction_id=auction_id)
