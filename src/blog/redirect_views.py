from django.shortcuts import redirect


def redirect_register(request):
    return redirect('accounts:register')


def redirect_login(request):
    return redirect('accounts:login')


def redirect_logout(request):
    return redirect('accounts:logout')


def redirect_reset(request):
    return redirect('accounts:resetPassword')


def redirect_forgot(request):
    return redirect('accounts:forgotPassword')
