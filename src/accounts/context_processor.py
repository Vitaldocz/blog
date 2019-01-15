from .forms import RegisterForm, LoginForm, ForgotPasswordForm


def register_form(request):
    if request.method == 'GET':
        form = RegisterForm()
        return {'register_form': form}


def login_form(request):
    if request.method == 'GET':
        form = LoginForm()
        return {'login_form': form}


def forgot_password(request):
    if request.method == 'GET':
        form = ForgotPasswordForm()
        return {'forgot_password_form': form}
