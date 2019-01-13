from __future__ import unicode_literals

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from . import redirect_views as redirect


urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls', namespace='accounts')),
    path('blog/', include('posts.urls', namespace='posts')),
    path('', include('home.urls', namespace='home')),

    # Permanent Redirects Do Not Edit
    path('register/', redirect.redirect_register, name='redirectRegister'),
    path('login/', redirect.redirect_login, name='redirectLogin'),
    path('logout/', redirect.redirect_logout, name='redirectLogout'),
    path('forgot-password/', redirect.redirect_forgot, name='redirectForgot'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
