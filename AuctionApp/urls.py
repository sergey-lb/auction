"""AuctionApp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views

from AuctionApp import settings
from auction import views as auction_views
from comment import views as comment_views
from photo import views as photo_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', auction_views.home, name='home'),
    path('auctions', auction_views.auctions, name='auctions'),
    path('user/<int:user_id>/auctions', auction_views.user_auctions, name='user_auctions'),
    path('auctions/<int:auction_id>', auction_views.auction, name='auction'),
    path('auctions/<int:auction_id>/edit', auction_views.auction_edit, name='auction_edit'),
    path('auctions/<int:auction_id>/save', auction_views.auction_save, name='auction_save'),
    path('auctions/<int:auction_id>/delete', auction_views.auction_delete, name='auction_delete'),
    path('auctions/<int:auction_id>/makebet', auction_views.make_bet, name='make_bet'),
    path('accounts/login/', auth_views.LoginView.as_view(redirect_authenticated_user=True)),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/', include('django_registration.backends.one_step.urls')),
    path('comments/<int:auction_id>/add', comment_views.comment_save, name='comment_save'),
    path('photo/<int:auction_id>/save', photo_views.photo_save, name='photo_save'),
    path('photo/<int:auction_id>/<int:photo_id>/delete', photo_views.photo_delete, name='photo_delete')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
