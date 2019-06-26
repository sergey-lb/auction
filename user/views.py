from django.http import HttpRequest
from django.shortcuts import render


# Create your views here.
def user_edit(request: HttpRequest, user_id: int):
    return render(
        request,
        template_name='user_edit.html',
        context={}
    )


def user_save(request: HttpRequest, user_id: int):
    return None

