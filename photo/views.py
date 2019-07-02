from django.http import HttpRequest
from django.http import JsonResponse
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt
from photo.forms import PhotoForm
from django.db import IntegrityError
from photo.models import Photo

# Create your views here.
@csrf_exempt
def photo_save(request: HttpRequest, auction_id: int):

    photo = Photo(auction_id=auction_id)
    form = PhotoForm(request.POST, request.FILES, instance=photo)
    if form.is_valid():
        try:
            form.save()
        except IntegrityError:
            return JsonResponse({'result': 0, 'msg': 'Ошибка загрузки файла'})
    else:
        return JsonResponse({'result': 0, 'msg': 'Ошибка загрузки файла'})

    return JsonResponse({'result': 1})


def photo_delete(request: HttpRequest, auction_id: int, photo_id: int):
    try:
        photo = Photo.objects.get(pk=photo_id)
        photo.delete()
    except Photo.DoesNotExist:
        pass

    return redirect('auction_edit', auction_id=auction_id)
