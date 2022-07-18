from django.shortcuts import redirect, render, HttpResponse, get_object_or_404
from random import choice
from django.contrib.auth.models import User
from django.core.mail import EmailMessage, send_mail
import smtplib, smtpd, string, os 
from email.message import EmailMessage
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import auth, messages
from django.contrib.auth import authenticate, login
from decouple import *
# Create your views here.

def index(request):
    return render(request, 'index.html')

def cadastro(request):
    if request.method == 'POST':
        name = str(request.POST [ 'name' ]).title().strip()
        email = str(request.POST [ 'email' ]).lower().strip()

        if email and name:        
            if User.objects.filter(email=email).exists():
                messages.error(request, 'Email ja cadastrado')
                return redirect('cadastro')
            tamanho = 6
            valores = string.digits
            password = ''        
            for i in range(tamanho):
                password += choice(valores)

            user = User.objects.create_user(username=email, email=email, first_name=name ,password=password )
            
            EMAIL_ADDRESS = config('EMAIL_BACKEND')
            EMAIL_PASSWORD = config('EMAIL_HOST_PASSWORD')
            msg = EmailMessage()
            msg['Subject'] = 'Cadastro Alura Bank'
            msg['From'] = config('EMAIL_BACKEND')
            msg['To']  = email
            msg.set_content(f'Olá {name} sua senha de acesso ao Alura Bank é {password}')
            with smtplib.SMTP_SSL('smtp.gmail.com',465) as smtp:
                smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
                smtp.send_message(msg)

            user.save()
            messages.success(request, 'Cadastro realizado com sucesso')
            return redirect('login')
        else:
            print('ola')
            messages.error(request, 'O email e nome não pode ficar em branco')
            return render(request, 'cadastro.html')  
    else:       
        return render(request, 'cadastro.html')

def login(request):

    if request.method == 'POST':       
    
        try:
            print('Request Valida')
            email = request.POST [ 'email' ]
            password = request.POST [ 'password' ]  
            
            if User.objects.filter(email=email).exists():
                print('Request Valida 2')
                nome = User.objects.filter(email=email).values_list('username', flat=True).get()
                user = auth.authenticate(request, username=nome, password=password)

                if user is not None:
                    auth.login(request, user)
                    messages.success(request, 'Login Realizado com sucesso.')
                    print('Login realizado com sucesso')
                    return redirect('transacoes')
                else:
                    messages.error(request, 'Senha Invalido')
                    
                    return render(request, 'login.html')

            else:
                messages.error(request, 'Email não cadastrado!')
                return redirect('cadastro')

        except ValueError:
            print('Usuario com Bloqueio')
            return render(request, 'login.html')
    else:
        print('POST Inválido')
        return render(request, 'login.html')
    
def logout(request):
    if not request.user.is_authenticated:

        return redirect('index')    
    if request.user.is_authenticated:
        messages.success(request, 'Loguot realizado com sucesso.')
        auth.logout(request)
        return redirect('index')





