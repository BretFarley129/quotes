# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages

import bcrypt

# Create your views here.

def index(request):
    if not "id" in request.session:
        request.session['id'] = ""
    return render(request,'belt/index.html')

def register(request):
    name = request.POST['name']
    alias = request.POST['alias']
    email = request.POST['email']
    password = request.POST['password']
    confirm = request.POST['confirm']
    birthday = request.POST['birthday']
    x = {'name': name,
         'alias': alias,
         'email': email,
         'password': password,
         'confirm': confirm,
         'birthday': birthday
    }
    errors = User.objects.validate(x)
    if errors:
        for tag, error in errors.iteritems():
            messages.error(request, error, extra_tags=tag)
        return redirect('/')
    else:
        hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        user = User.objects.create(name = name, alias = alias, email = email, password = hashed_password, birthday = birthday)
        request.session['id'] = User.objects.filter(email=request.POST['email'])[0].id
        return redirect('/quotes')

def login(request):
    email = request.POST['email']
    password = request.POST['password']
    hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    try:
        user = User.objects.filter(email = email)[0]
        hash1 = user.password
    except:
        hash1 = request.POST['email']


    x = { 'email': email, 'password': password, 'hash1' : hash1}
    errors = User.objects.validateLogin(x)
    if errors:
        for tag, error in errors.iteritems():
            messages.error(request, error, extra_tags=tag)
        return redirect('/')
    else:
        request.session['id'] = User.objects.filter(email=request.POST['email'])[0].id
        return redirect('/quotes')


def add(request):
    quoted_by = request.POST['quoted_by']
    message = request.POST['message']
    currentUser = User.objects.get(id = request.session['id'])
    x = {
        'quoted_by': quoted_by,
        'message': message,
    }
    errors = Quote.objects.validate(x)
    if errors:
        for tag, error in errors.iteritems():
            messages.error(request, error, extra_tags=tag)
    else:
        Quote.objects.create(quoted_by = quoted_by, message = message, posted_by = currentUser)
    return redirect('/quotes')

def logout(request):
    request.session['id'] = ""
    return redirect('/')



def quotes(request):
    if not request.session['id']:
        messages.add_message(request, messages.INFO, 'You must be logged in to see this content')
        return redirect('/')
        
    user = User.objects.get(id = request.session['id'])
    context = {}
    context['name'] = User.objects.get(id = request.session['id']).alias
    context['stuff'] = Quote.objects.exclude(favorited_by = user)
    context['liked'] = user.favorites.all()
    return render(request,'belt/quotes.html',context)

def users(request, number):
    if not request.session['id']:
        messages.add_message(request, messages.INFO, 'You must be logged in to see this content')
        return redirect('/')
    context = {}
    theUser = User.objects.get(id = number)
    context['stuff'] = theUser
    context['tot'] = len(Quote.objects.filter(posted_by = theUser))
    context['quotes'] = Quote.objects.filter(posted_by = theUser)
    return render(request, 'belt/users.html', context)

def favorite(request, number):
    user = User.objects.get(id = request.session['id'])
    quote = Quote.objects.get(id = number)
    quote.favorited_by.add(user)
    quote.save()
    
    return redirect('/quotes')

def remove(request, number):
    user = User.objects.get(id = request.session['id'])
    quote = Quote.objects.get(id = number)
    quote.favorited_by.remove(user)
    quote.save()
    
    return redirect('/quotes')







