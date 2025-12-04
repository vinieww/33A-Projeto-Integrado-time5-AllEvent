

from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Evento 
from django.shortcuts import render, get_object_or_404

def home(request):

    eventos_recentes = Evento.objects.order_by('-data')[:8]
    contexto = {
        'eventos_carousel': eventos_recentes
    }
    return render(request, 'core/home.html', contexto)


def cadastro(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        nome = request.POST.get('nome_completo')
        email = request.POST.get('email')
        senha = request.POST.get('password')
        senha_confirm = request.POST.get('password_confirm')

        if senha != senha_confirm:
            messages.error(request, 'As senhas não coincidem!')
            return redirect('cadastro')
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Este e-mail já está em uso.')
            return redirect('cadastro')
        
        user = User.objects.create_user(username=email, email=email, password=senha)
        user.first_name = nome
        user.save()
        login(request, user)
        messages.success(request, 'Conta criada com sucesso!')
        return redirect('home')
    return render(request, 'core/cadastro.html') 

@login_required
def perfil_view(request):
    return render(request, 'core/perfil.html') 

@login_required
def editar_dados(request):
    if request.method == 'POST':

        senha_atual = request.POST.get('current_password')
        nome_completo = request.POST.get('name')
        email = request.POST.get('email')
        nova_senha = request.POST.get('password')

        if not request.user.check_password(senha_atual):
            messages.error(request, 'A senha atual está incorreta. Nenhuma alteração foi salva.')
            return redirect('editar_dados')

        request.user.first_name = nome_completo

        if email and email != request.user.email:
            if User.objects.filter(email=email).exclude(pk=request.user.pk).exists():
                messages.error(request, 'Este e-mail já está sendo usado por outra conta.')
                return redirect('editar_dados')
            request.user.email = email
            request.user.username = email

        if nova_senha:
            request.user.set_password(nova_senha)

        request.user.save()

        messages.success(request, 'Seus dados foram atualizados com sucesso!')
        return redirect('editar_dados')
    
    return render(request, 'core/editar_dados.html')

@login_required
def favoritos_view(request):
    return render(request, 'core/favoritos.html')

@login_required
def preferencias_view(request):
    return render(request, 'core/preferencias.html')


def lista_eventos(request):
    todos_os_eventos = Evento.objects.order_by('-data')
    contexto = {'eventos': todos_os_eventos}
    return render(request, 'core/lista_eventos.html', contexto)

def buscar_eventos(request):
    return render(request, 'core/buscar_eventos.html')

def resultado_busca(request):
    termo = request.GET.get('termo_busca', '')
    if termo:
        eventos_filtrados = Evento.objects.filter(nome__icontains=termo)
    else:
        eventos_filtrados = []
    contexto = {'eventos': eventos_filtrados, 'termo_busca': termo}
    return render(request, 'core/lista_eventos.html', contexto)


def detalhe_evento(request, evento_id):
    evento = get_object_or_404(Evento, pk=evento_id)
    
    contexto = {
        'evento': evento
    }
    return render(request, 'core/detalhe_evento.html', contexto)