from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.views.decorators.cache import never_cache 
from django.utils.decorators import method_decorator
from django.db.models import Q 
from .models import Evento, Avaliacao, Categoria, Comentario,Preferencia
from django.db.models import Avg
from django.core.exceptions import ObjectDoesNotExist

def home(request):
    # 1. Começa com todos os eventos (Padrão)
    queryset = Evento.objects.all()
    titulo_secao = "Eventos em Destaque"
    
    # 2. Tenta personalizar se estiver logado
    if request.user.is_authenticated:
        try:
            # Tenta acessar as preferências do usuário
            # Se der erro aqui, é porque o usuário nunca salvou preferências
            pref = request.user.preferencias 
            
            interesses = pref.interesses.all()
            
            # Se ele marcou interesses
            if interesses.exists():
                print(f"DEBUG: O usuário {request.user} gosta de: {interesses}")
                
                # Filtra os eventos
                eventos_filtrados = queryset.filter(categoria__in=interesses)
                
                # AQUI ESTÁ O SEGREDO:
                # Só aplicamos o filtro se existirem eventos daquelas categorias.
                if eventos_filtrados.exists():
                    queryset = eventos_filtrados
                    titulo_secao = f"Recomendados para {request.user.first_name or request.user.username}"
                else:
                    print("DEBUG: Usuário tem interesses, mas não existem eventos dessas categorias no banco.")
                    # O código continua usando o 'queryset' original (todos os eventos)
            else:
                print("DEBUG: Usuário tem preferência salva, mas não marcou nenhuma caixa.")

        except ObjectDoesNotExist:
            print("DEBUG: Usuário logado, mas nunca salvou preferências (Objeto não existe).")
        except AttributeError:
            print("DEBUG: Erro de configuração no Model. Verifique o related_name='preferencias'.")

    # 3. Aplica a aleatoriedade e o limite
    eventos_carousel = queryset.order_by('?')[:15]

    contexto = {
        'eventos_carousel': eventos_carousel,
        'titulo_secao': titulo_secao
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
    # Garante que o usuário tenha um objeto de preferências (cria se não existir)
    preferencia, created = Preferencia.objects.get_or_create(usuario=request.user)
    
    # Busca todas as categorias para montar o formulário
    todas_categorias = Categoria.objects.all()

    if request.method == 'POST':
        # 1. Atualiza Cidade e Email
        preferencia.cidade_padrao = request.POST.get('cidade_padrao', '')
        preferencia.receber_emails = request.POST.get('receber_emails') == 'on'
        
        # 2. Atualiza os Interesses (ManyToMany é um pouco diferente)
        # Limpa os interesses atuais e adiciona os marcados
        preferencia.interesses.clear()
        ids_categorias = request.POST.getlist('interesses') # Pega lista de checkboxes
        for cat_id in ids_categorias:
            preferencia.interesses.add(cat_id)
            
        preferencia.save()
        messages.success(request, 'Preferências salvas com sucesso!')
        return redirect('preferencias')

    contexto = {
        'pref': preferencia,
        'categorias': todas_categorias
    }
    return render(request, 'core/preferencias.html', contexto)


def lista_eventos(request):
    todos_os_eventos = Evento.objects.order_by('-data')
    contexto = {'eventos': todos_os_eventos}
    return render(request, 'core/lista_eventos.html', contexto)

def buscar_eventos(request):
    categorias = Categoria.objects.all()
    contexto = {'categorias': categorias}
    return render(request, 'core/buscar_eventos.html', contexto)

def resultado_busca(request):
    termo = request.GET.get('termo_busca', '')
    local = request.GET.get('local', '')
    data = request.GET.get('data', '')
    categoria_id = request.GET.get('categoria', '')
    avaliacao_minima = request.GET.get('avaliacao', '')

    eventos = Evento.objects.all().order_by('-data')
    
    if termo:
        eventos = eventos.filter(nome__icontains=termo)
    
    if local:
        eventos = eventos.filter(local__icontains=local)
    
    if data:
        # Filtra pela data exata
        eventos = eventos.filter(data__date=data)
    
    if categoria_id:
        eventos = eventos.filter(categoria_id=categoria_id)

    # 4. Filtro especial de Avaliação (Média)
    if avaliacao_minima:
        # Primeiro calculamos a média de cada evento, depois filtramos
        try:
            nota = int(avaliacao_minima)
            eventos = eventos.annotate(media_notas=Avg('avaliacoes__nota')).filter(media_notas__gte=nota)
        except ValueError:
            pass # Se o valor não for número, ignora

    contexto = {
        'eventos': eventos,
        'termo_busca': termo # Para manter o termo na barra de busca se quiser
    }
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
    
    minha_avaliacao = None
    if request.user.is_authenticated:
        avaliacao_obj = Avaliacao.objects.filter(evento=evento, usuario=request.user).first()
        if avaliacao_obj:
            minha_avaliacao = avaliacao_obj.nota
    
    media = evento.avaliacoes.aggregate(Avg('nota'))['nota__avg']
    media = round(media, 1) if media else 0
    
    comentarios = evento.comentarios.all().order_by('-data_criacao')

    contexto = {
        'evento': evento,
        'compact_header': True,
        'esta_favoritado': esta_favoritado,
        'minha_avaliacao': minha_avaliacao,
        'media_geral': media,
        'comentarios': comentarios,
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

@login_required
def avaliar_evento(request, evento_id):
    if request.method == 'POST':
        evento = get_object_or_404(Evento, pk=evento_id)
        nota = request.POST.get('nota')
        
        if nota:
            # Cria ou atualiza a avaliação do usuário
            Avaliacao.objects.update_or_create(
                evento=evento,
                usuario=request.user,
                defaults={'nota': nota}
            )
        
    return redirect('detalhe_evento', evento_id=evento_id)

@login_required
def adicionar_comentario(request, evento_id):
    evento = get_object_or_404(Evento, pk=evento_id)
    
    if request.method == 'POST':
        texto = request.POST.get('comentario_texto')
        
        if texto:
            Comentario.objects.create(
                evento=evento,
                usuario=request.user,
                texto=texto
            )
            # Não precisa de mensagem de sucesso para comentários rápidos, 
            # mas se quiser, pode usar messages.success
            
    return redirect('detalhe_evento', evento_id=evento_id)

@login_required
def deletar_comentario(request, comentario_id):
    # Busca o comentário ou dá erro 404 se não existir
    comentario = get_object_or_404(Comentario, pk=comentario_id)
    
    # Salva o ID do evento para redirecionar depois
    evento_id = comentario.evento.id
    
    # SEGURANÇA: Só apaga se o usuário logado for o dono do comentário
    if request.user == comentario.usuario or request.user.is_staff:
        comentario.delete()
        # Opcional: messages.success(request, "Comentário excluído.")
    else:
        # Opcional: messages.error(request, "Você não tem permissão para excluir este comentário.")
        pass

    return redirect('detalhe_evento', evento_id=evento_id)