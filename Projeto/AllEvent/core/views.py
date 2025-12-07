from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.views.decorators.cache import never_cache # Corrigido (estava never_cachea)
from django.utils.decorators import method_decorator
from django.db.models import Q # NOVO: Necessário para fazer a busca "OU" (Nome OU Categoria)
from .models import Evento

def home(request):
    eventos_recentes = Evento.objects.order_by('-data')[:8]
    contexto = {
        'eventos_carousel': eventos_recentes
    }
    return render(request, 'core/home.html', contexto)

@never_cache
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

    contexto = {
        'compact_header': True,      
        'hide_header_buttons': True
    }
    
    return render(request, 'core/cadastro.html', contexto)

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
    eventos_favoritados = request.user.eventos_favoritos.all()
    
    contexto = {
        'eventos': eventos_favoritados
    }
    return render(request, 'core/favoritos.html', contexto)

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
        # ATUALIZAÇÃO IMPORTANTE:
        # Busca no nome do evento OU ( | ) no nome da categoria
        eventos_filtrados = Evento.objects.filter(
            Q(nome__icontains=termo) | 
            Q(categoria__nome__icontains=termo)
        )
    else:
        eventos_filtrados = []
        
    contexto = {'eventos': eventos_filtrados, 'termo_busca': termo}
    
    # Mudei aqui para renderizar o arquivo novo que criamos (resultado_busca.html)
    return render(request, 'core/resultado_busca.html', contexto)

@never_cache
def detalhe_evento(request, evento_id):
    evento = get_object_or_404(Evento, pk=evento_id)
    
    if request.GET.get('erro') == 'login':
        messages.error(request, "Você precisa estar logado para favoritar eventos.")

    esta_favoritado = False
    if request.user.is_authenticated:
        if evento.favoritos.filter(id=request.user.id).exists():
            esta_favoritado = True
    
    contexto = {
        'evento': evento,
        'compact_header': True,
        'esta_favoritado': esta_favoritado
    }
    return render(request, 'core/detalhe_evento.html', contexto)

def toggle_favorito(request, evento_id):
    evento = get_object_or_404(Evento, pk=evento_id)
    
    if not request.user.is_authenticated:
        url = reverse('detalhe_evento', args=[evento_id])
        return redirect(f'{url}?erro=login')

    if evento.favoritos.filter(id=request.user.id).exists():
        evento.favoritos.remove(request.user)
    else:
        evento.favoritos.add(request.user)

    return redirect('detalhe_evento', evento_id=evento_id)