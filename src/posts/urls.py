from __future__ import unicode_literals

from django.urls import path
from django.views.generic import RedirectView
from . import views as posts

app_name = 'posts'


urlpatterns = [
    path('', RedirectView.as_view(url='/')),
    path('<str:slug>', posts.DetailView.as_view(), name='detailView')
]