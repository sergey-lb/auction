from django.http import HttpRequest
from django.shortcuts import redirect
from AuctionApp import settings


def redirect_authenticated_user(view):
    def wrapper_function(request: HttpRequest, *args, **kwargs):
        if not request.user.is_anonymous:
            return redirect(settings.LOGIN_REDIRECT_URL)
        return view(request, *args, **kwargs)
    wrapper_function.view_name = ".".join((view.__module__, view.__name__))
    return wrapper_function
