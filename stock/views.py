from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.contrib.auth.models import User
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_text
from django.utils.encoding import force_bytes
from stock.forms import SignUpForm
from stock.tokens import account_activation_token
from django.contrib.auth import login, authenticate
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect

import datetime as dt
import matplotlib.pyplot as plt
from matplotlib import style
import pandas as pd
import requests
from pandas_datareader import data as web

from django.shortcuts import render


def main(request):
    return render(request, 'stock/login.html', {})


def index(request):
    return render(request, 'stock/index.html', {})


def login(request):
    return render(request, 'stock/index.html', {})


def fetch_data(request):
    style.use('ggplot')

    start = dt.datetime(2017, 11, 1)
    end = dt.datetime(2017, 12, 31)

    df = web.DataReader('TSLA', 'yahoo', start, end)
    context = {'data_frame': df.to_dict()}
    print(context)
    return render(request, 'stock/stocks_raw.html', context)


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            subject = 'Activate Your MySite Account'
            message = render_to_string('stock/account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            user.email_user(subject, message)
            return redirect('account_activation_sent')
    else:
        form = SignUpForm()
    return render(request, 'stock/signup.html', {'form': form})


def account_activation_sent(request):
    return render(request, 'stock/account_activation_sent.html')


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.profile.email_confirmed = True
        user.save()
        login(request, user)
        return redirect('home')
    else:
        return render(request, 'stock/account_activation_invalid.html')
