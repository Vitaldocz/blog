from .forms import RegisterForm, LoginForm


def register_form(request):
    if request.method == 'GET':
        form = RegisterForm()
        return {'register_form': form}


def login_form(request):
    if request.method == 'GET':
        form = LoginForm()
        return {'login_form': form}
