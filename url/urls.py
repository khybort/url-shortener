# /url/urls.py
from django.urls import path

from url import views

urlpatterns = [
    # ...
    path('url/', views.create_short_url),
    path('url/stats/<str:hash>/', views.get_url_stats),
    path('url/<str:hash>/', views.redirect_original_url),
    # ...
]