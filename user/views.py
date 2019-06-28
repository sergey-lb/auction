from django.http import HttpRequest
from django.shortcuts import render, redirect
from django_registration.backends.one_step.views import RegistrationView


# Create your views here.
def user_edit(request: HttpRequest, user_id: int):
    return render(
        request,
        template_name='user_edit.html',
        context={}
    )


def user_save(request: HttpRequest, user_id: int):
    return None
