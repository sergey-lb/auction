from django.http import HttpRequest
from django.shortcuts import render


# Create your views here.
def user(request: HttpRequest, user_id: int):
    return render(
        request,
        template_name='user.html',
        context={}
    )

