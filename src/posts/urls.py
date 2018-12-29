from __future__ import unicode_literals

from django.urls import path
from . import views as posts

app_name = 'posts'


urlpatterns = [
    path('', posts.BlogIndexView.as_view(), name='indexView'),
    path('<str:slug>', posts.BlogDetailView.as_view(), name='detailView')
]