from django.urls import path
from . import views


app_name = 'accounts'

urlpatterns = [
    path('', views.RedirectRegisterView.as_view(), name='redirectRegister'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('forgot-password/', views.ForgotPasswordView.as_view(), name='forgotPassword'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('verify/<str:email>/<str:token>', views.VerificationView.as_view(), name='verify'),
]
