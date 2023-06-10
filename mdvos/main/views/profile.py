# -*- coding: utf-8 -*-

from django.shortcuts import render, redirect
import datetime
from ..forms import EditUserForm
from main.models.models import User
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate
import chardet

def profile(request):
    if not request.user.is_authenticated:
        request.session['next_page'] = request.get_full_path()
        return redirect('login')
    
    # first_name = request.user.first_name 
    # first_name_c = first_name[2:-1]
    # first_name_dec = bytes.fromhex(first_name_c).decode('utf-8')
    # print(first_name) 
    # first_name_dec = first_name.decode('utf-8')
    # encoding = chardet.detect(bytes(first_name, 'utf-8'))["encoding"]
    # first_name_dec = first_name.encode(encoding).decode("utf-8")
    form = EditUserForm()
    context = {
        'form': form,
        #'first_name': first_name
    }

    if request.method == "POST":       
        if "save_password_change" in request.POST:

                old_password = request.POST['old_password']
                if request.user.check_password(old_password):

                    new_password1 = request.POST['password1']
                    new_password2 = request.POST['password2']
                    if new_password1 == new_password2:
                        request.user.set_password(new_password1)
                        request.user.save()
                        update_session_auth_hash(request, request.user)
                        messages.success(request, 'Twoje hasło zostało zmienione.')
                        return redirect('profile')
                    else:
                        messages.error(request, 'Podane hasła nie są identyczne.')
                        return redirect('profile')


        elif "save_edit" in request.POST:
            user = request.user
            print("przed sprawdzeniem")
            # nie działają polskie znaki
            
            if len(request.POST['first_name']):
                user.first_name = request.POST['first_name']
                # user.first_name = user.first_name.encode('utf-8')
                user.save()
            
            if len(request.POST['last_name']):
                user.last_name = request.POST['last_name']
                user.save()
            
            if len(request.POST['username']):
                new_username = request.POST['username']

                if User.objects.filter(username=new_username).exists():
                    messages.error(request, "Nazwa użytkownika już istnieje")
                else:
                    user.username = new_username
                    user.save()

            if len(request.POST['email']):
                new_email = request.POST['email']

                if User.objects.filter(email=new_email).exists():
                    pass
                else:
                    user.email = new_email  
                    user.save()

            
            

    return render(request, "profile.html", context)



