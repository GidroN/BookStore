from django.urls import path

from store.views import auth

urlpatterns = [
    path('auth/', auth)
]