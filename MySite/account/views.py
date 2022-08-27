from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth import authenticate, login, get_user_model
from .forms import LoginForm
from django.contrib.auth.decorators import login_required
#from django_user_interaction_log import create_log_record
from  django_user_interaction_log.registrars import create_log_record

# Create your views here.
def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request,
                                username=cd['username'],
                                password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponse('Authenticated successfully')
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid login')
    else:
        form = LoginForm()
    create_log_record(request=request, log_detail='The user has logged in')
    return render(request, 'account/login.html', {'form': form})


@login_required
def dashboard(request):
    return render(request,
                  'account/dashboard.html',
                  {'section': 'dashboard'})

