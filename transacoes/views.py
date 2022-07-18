from random import choice
import smtplib, smtpd, string, os 
from email.message import EmailMessage
from django.shortcuts import redirect, render, HttpResponse
from django.contrib.auth.models import User
from csv import reader
from django.http import FileResponse
from .models import  Controller, ImportacoesArquivos
from django.views.generic import DetailView, ListView
from django.db import IntegrityError
from django.core.exceptions import ValidationError
from django.utils.datastructures import MultiValueDictKeyError
from django.db.models import Sum, Min, Max, Count
from django.contrib import auth, messages
from xml.dom import minidom
import xml.etree.ElementTree as ET
from collections import defaultdict
import json

def transacoes(request):    

    if request.user.is_authenticated:
        lista_informacao_arquivo = ImportacoesArquivos.objects.all().order_by('-data_transacao_arquivo')
        lista_conteudo_arquivo = Controller.objects.all().order_by('data_da_transacao')       
    
        dados = { 
        'lista_informacao_arquivo': lista_informacao_arquivo,
        'lista_conteudo_arquivo': lista_conteudo_arquivo, 
        }
        if request.method == 'POST':

            if '.csv' in str(request.FILES['file_name']):

                validado = list(reader(list(FileResponse(request.FILES['file_name']))[0].decode('utf-8').split('\n')))
                print('************************************')  
                
                nome_arquivo = request.FILES['file_name']
                print('Nome do Arquivo', request.FILES['file_name'])  
                tamanho_arquivo = request.FILES['file_name'].size/1000000,'megabytes'
                print('Tamanho do Arquivo', request.FILES['file_name'].size/1000000,'megabytes')
                data_transacao_arquivo = (validado[0][7])[:10]  
                print('Quantidade de Linhas',len(validado))      
                print('**********************************')

                try:
                    if not ImportacoesArquivos.objects.filter(       
                                        data_transacao_arquivo = data_transacao_arquivo,
                                        ).exists():

                        operacao02 = ImportacoesArquivos(nome_arquivo = nome_arquivo,
                                                        tamanho_arquivo = tamanho_arquivo,
                                                        data_transacao_arquivo = data_transacao_arquivo,
                                                        usuario_importacao_arquivo = request.user)                      
                        

                        for contador in (range(len(validado))):

                            print('****************************')
                            print('Linha', contador)
                            if (len(validado[contador])) == 8:
                                if (validado[contador][0].strip() != '' and
                                    validado[contador][1].strip() != '' and 
                                    validado[contador][2].strip() != '' and
                                    validado[contador][3].strip() != '' and
                                    validado[contador][4].strip() != '' and
                                    validado[contador][5].strip() != '' and
                                    validado[contador][6].strip() != '' and
                                    validado[contador][7].strip() != '') : 
                                    print('Validação: Arquivo com todos os Campos')
                                    
                                    if not Controller.objects.filter(       
                                                    banco_origem = (validado[contador][0]),
                                                    agencia_origem = (validado[contador][1]),
                                                    conta_origem = (validado[contador][2]),

                                                    banco_destino = (validado[contador][3]),
                                                    agencia_destino = (validado[contador][4]),
                                                    conta_destino = (validado[contador][5]),

                                                    valor_da_transacao = (float((validado[contador][6]))),
                                                    data_da_transacao = (validado[contador][7])[:10],
                                                    hora_da_transacao = (validado[contador][7])[11:],
                                                    ).exists():

                                        print('Valido: Operação cadastrada.')

                                        if data_transacao_arquivo == ((validado[contador][7])[:10]):
                                            print('Validado: Arquivo com data Validada')
                                            operacao02.save()
                                            operacao = Controller(
                                                banco_origem = (validado[contador][0]),
                                                agencia_origem = (validado[contador][1]),
                                                conta_origem = (validado[contador][2]),

                                                banco_destino = (validado[contador][3]),
                                                agencia_destino = (validado[contador][4]),
                                                conta_destino = (validado[contador][5]),
                                                                    
                                                valor_da_transacao = (float((validado[contador][6]))),                                                                                        
                                                data_da_transacao = (validado[contador][7])[:10],
                                                hora_da_transacao = (validado[contador][7])[11:],
                                                id_arquivo = operacao02                                      
                                                )
                                            operacao.save()
                                            
                                        else: 
                                            print('Erro: Linha com data divergente')
                                            print(validado[contador])
                                            
                                    else:
                                        print('Erro: Arquivo ja cadastrado')
                                        print(validado[contador])
                                        
                                else:
                               
                                    print('Erro: Arquivo faltando dados.')
                                    print(validado[contador])
                                    
                            else:
                                print('Erro: Arquivo Incompleto.')
                                
                       
                        return render(request, 'transacoes.html', dados)        
                    else: 
                        messages.error(request, 'Arquivo ja Importado')
                        return render(request, 'transacoes.html', dados)   

                except (UnicodeDecodeError, ValidationError, IndexError, MultiValueDictKeyError):
                    print('Arquivo com formato invalido')
                    return render(request, 'transacoes.html', dados)   
            

            if '.xml' in str(request.FILES['file_name']):

                tree = ET.parse(request.FILES['file_name'])
                root = tree.getroot()
                
                nome_arquivo = request.FILES['file_name']
                print('Nome do Arquivo', request.FILES['file_name'])  
                tamanho_arquivo = request.FILES['file_name'].size/1000000,'megabytes'
                print('Tamanho do Arquivo', request.FILES['file_name'].size/1000000,'megabytes')
                data_transacao_arquivo = ((root[0][3].text)[:10]) 
                print('Quantidade de Linhas',len(root))      
                print('**********************************')
                try:
                    if not ImportacoesArquivos.objects.filter(       
                                        data_transacao_arquivo = data_transacao_arquivo,
                                        ).exists():

                        operacao02 = ImportacoesArquivos(nome_arquivo = nome_arquivo,
                                                        tamanho_arquivo = tamanho_arquivo,
                                                        data_transacao_arquivo = data_transacao_arquivo,
                                                        usuario_importacao_arquivo = request.user)                      
                        

                        for contador in (range(len(root))):

                            print('****************************')
                            print('Linha', contador)
                            
                            if (root[contador][0][0].text.strip() != '' and
                                    root[contador][0][1].text.strip() != '' and 
                                    root[contador][0][2].text.strip() != '' and
                                    root[contador][1][0].text.strip() != '' and
                                    root[contador][1][1].text.strip() != '' and
                                    root[contador][1][2].text.strip() != '' and
                                    root[contador][2].text.strip() != '' and
                                    root[contador][3].text.strip() != '') : 
                                print('Validação: Arquivo com todos os Campos')

                                
             

                                if not Controller.objects.filter(       
                                                    banco_origem = (root[contador][0][0].text),
                                                    agencia_origem = (root[contador][0][1].text),
                                                    conta_origem = (root[contador][0][2].text),

                                                    banco_destino = (root[contador][1][0].text),
                                                    agencia_destino = (root[contador][1][1].text),
                                                    conta_destino = (root[contador][1][2].text),

                                                    valor_da_transacao = (float(root[contador][2].text)),
                                                    data_da_transacao = (root[contador][3].text)[:10],
                                                    hora_da_transacao = (root[contador][3].text)[11:],
                                                    ).exists():

                                    print('Valido: Operação cadastrada.')
                                    
                                    if data_transacao_arquivo == (root[contador][3].text)[:10]:
                                        print('Validado: Arquivo com data Validada')
                                        operacao02.save()
                                        operacao = Controller(
                                                banco_origem = (root[contador][0][0].text),
                                                agencia_origem = (root[contador][0][1].text),
                                                conta_origem = (root[contador][0][2].text),

                                                banco_destino = (root[contador][1][0].text),
                                                agencia_destino = (root[contador][1][1].text),
                                                conta_destino = (root[contador][1][2].text),
                                                                    
                                                valor_da_transacao = (float(root[contador][2].text)),                                                                                        
                                                data_da_transacao = (root[contador][3].text)[:10],
                                                hora_da_transacao = (root[contador][3].text)[11:],
                                                id_arquivo = operacao02                                      
                                                )
                                        operacao.save()
   
                                        print('Banco Origem',root[contador][0][0].text) # Banco Origem
                                        print('Agencia Origem',root[contador][0][1].text) # Agencia Origem
                                        print('Conta Origem',root[contador][0][2].text) # Conta Origem

                                        print('Banco Destino',root[contador][1][0].text) # Banco Destino
                                        print('Agencia Destino',root[contador][1][1].text) # Agencia Destino
                                        print('Conta Origem',root[contador][1][2].text) # Conta Origem

                                        print('Valor da Transação',root[contador][2].text) # Valor da Transação
                                        print('Hora da Transação',(root[contador][3].text)[11:]) # Hora da Transação
                                        print('Data da Transação',(root[contador][3].text)[:10]) # Data da Transação
                                        print('***************************') 
                                            
                                    else: 
                                        print('Erro: Linha com data divergente')
                                        print(root[contador])
                                            
                                else:
                                    print('Erro: Arquivo ja cadastrado')
                                    print(root[contador])
                                        
                            else:
                                print('Erro: Arquivo faltando dados.')
                                print(root[contador])
                                    
                            
                        return render(request, 'transacoes.html', dados)        
                    else: 
                        messages.error(request, 'Arquivo ja Importado')
                        print('Erro: Arquivo ja Importado')
                        return render(request, 'transacoes.html', dados)   

                except (UnicodeDecodeError, ValidationError, IndexError, MultiValueDictKeyError):
                    print('Arquivo com formato invalido')
                    return render(request, 'transacoes.html', dados)   
     
            else:
                print('Arquivo diferente de CSV/XML')
                return render(request, 'transacoes.html', dados)                
                            

        else:
            print('Erro: Request POST invalida ')
            return render(request, 'transacoes.html', dados)   
            
    else:
        print('Erro: Usuario Não Autenticado')
        return redirect( 'login')            

def analise_de_transacoes(request):
    if request.user.is_authenticated:
        if request.method == "POST":
                           
            if request.POST ['data_inicial'] <= request.POST ['data_final']:

                
                ## Transações Suspeitas ##
                transacoes_suspeitas = (Controller.objects.order_by('banco_origem', 'agencia_origem', 'conta_origem', 'data_da_transacao', 'hora_da_transacao').filter(valor_da_transacao__gte= 5000,
                                                            data_da_transacao__gte= request.POST ['data_inicial'], 
                                                            data_da_transacao__lte = request.POST ['data_final']).
                                                            values_list('banco_origem', 'agencia_origem', 'conta_origem', 
                                                                        'banco_destino', 'agencia_destino', 'conta_destino',
                                                                        'valor_da_transacao', 'hora_da_transacao', 'data_da_transacao'))
                
                ## Contas Suspeitas ##                    
                contas_suspeitas = (Controller.objects.filter(
                                                            data_da_transacao__gte= request.POST ['data_inicial'], 
                                                            data_da_transacao__lte = request.POST ['data_final']).values_list('banco_origem', 'agencia_origem', 'conta_origem').annotate(Sum('valor_da_transacao')))
                ## Agencias Suspeitas ## 
                agencias_suspeitas = (Controller.objects.filter(
                                                            data_da_transacao__gte= request.POST ['data_inicial'], 
                                                            data_da_transacao__lte = request.POST ['data_final']).values_list('banco_origem', 'agencia_origem').annotate(Sum('valor_da_transacao'))) 
                analises = { 
                        'transacoes_suspeitas': transacoes_suspeitas,
                        'contas_suspeitas' : contas_suspeitas,
                        'agencias_suspeitas' : agencias_suspeitas,
                        }
                if not transacoes_suspeitas and not contas_suspeitas and not agencias_suspeitas:
                    datas_transações_minima = (ImportacoesArquivos.objects.order_by('data_transacao_arquivo').
                                                            values_list('data_transacao_arquivo').
                                                            annotate(Min('data_transacao_arquivo')))
                    
                    datas_transações_maxima = (ImportacoesArquivos.objects.order_by('-data_transacao_arquivo').
                                                            values_list('data_transacao_arquivo').
                                                            annotate(Max('data_transacao_arquivo')))
                                                        
                    messages.warning(request, f'Não existe operações nesse periodo. Verifique as datas entre {(datas_transações_minima[0][0].strftime("%d-%b-%Y"))} à {datas_transações_maxima[0][0].strftime("%d-%b-%Y")}.')
                    
                     
                return render(request, 'analise_de_transacoes.html', analises)
              
                    
            else:
                messages.warning(request, 'A data inicial deve ser menor que a data final')
                return render(request, 'analise_de_transacoes.html')
        else:
            
            return render(request, 'analise_de_transacoes.html')
    else:
        return render(request, 'login.html')

def usuarios(request):
    if request.user.is_authenticated: 
 
        if  request.user != list(User.objects.all()):
            dados_usuario = request.user
            dados_usuarios = list(User.objects.all().order_by('first_name'))
            try:
                while True:
                    dados_usuarios.remove(dados_usuario)

                    
            except ValueError:
                pass
            
            lista_usuarios = dados_usuarios
            lista_usuarios = lista_usuarios

            dados_usuarios = {
            'lista_usuarios': lista_usuarios,
                    }  
                    
        else:
            
            print(f'Usaurio autenticado')
        return render(request, 'usuarios.html', dados_usuarios) 

    else:
        return render(request, 'login.html')

def delete_user(request):
    if request.user.is_authenticated: 

         if  request.user != list(User.objects.all()):

            if request.method == 'POST':

                delete_usur = (list(request.POST)[1])

                print('*****')
                print(delete_usur)
                record = User.objects.get(id = int(delete_usur))
                print(record.is_active)
                record.is_active = False
                print(record.is_active)

                record.save()
                messages.warning(request, 'Usuário Deletado.')
            return redirect('usuarios')


    else:
        return redirect('usuarios')    

def update_user(request):

    try:
        if request.user.is_authenticated: 

            if  request.user != list(User.objects.all()):

                if request.method == 'POST':
                    
                        update_usuario_id = (list(request.POST)[3])
                        print(update_usuario_id)

                        update_usuario_first_name = (str(request.POST['first_name']).title().strip())
                    
                        update_usuario_email = (str(request.POST['email']).lower().strip())
                        
                        update_usuario_username = (request.POST['email'])                        

                        user = User.objects.get(id=update_usuario_id)
                        user.username = update_usuario_username               
                        user.email = update_usuario_email               
                        user.first_name = update_usuario_first_name
                        
                    
                        user.save()
                        messages.success(request, 'Usuário atualizado com sucesso.')
                        return redirect('usuarios')
                    
                        
            

                else:
                    print('Usuario não autorizado')
                    return redirect('usuarios')
            

        else:
            print('Usuario não autorizado')
            return redirect('usuarios') 
    except IntegrityError:
      
        return redirect('usuarios')

def new_user(request):
    if request.user.is_authenticated:

        if request.method == 'POST':
            name = str(request.POST [ 'name' ]).title().strip()
            email = str(request.POST [ 'email' ]).lower().strip()

            if email and name:   
                     
                if not User.objects.filter(email=email, username=email).exists():
                    
                    
                    tamanho = 6
                    valores = string.digits
                    password = ''        
                    for i in range(tamanho):
                        password += choice(valores)

                    user = User.objects.create_user(username=email, email=email, first_name=name ,password=password )
                    
                    EMAIL_ADDRESS = 'x email '
                    EMAIL_PASSWORD = 'x senha '
                    msg = EmailMessage()
                    msg['Subject'] = 'Cadastro Alura Bank'
                    msg['From'] = 'x email'
                    msg['To']  = email
                    msg.set_content(f'Olá {name} sua senha de acesso ao Alura Bank é {password}')
                    with smtplib.SMTP_SSL('smtp.gmail.com',465) as smtp:
                        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
                        smtp.send_message(msg)

                    user.save()
                    messages.success(request, 'Cadastro realizado com sucesso')

                else:
                    messages.error(request, 'Email ja cadastrado')
                    return redirect('usuarios')
               
            else:
                print('ola')
                messages.error(request, 'O email e nome não pode ficar em branco')
                return render(request, 'usuarios.html')  
        else:       
            return render(request, 'usuarios.html')
        
    else:

        return redirect('usuarios')


