# Arquivo: AllEvent/AllEvent/urls.py

from django.contrib import admin
from django.urls import path, include
from core import views
from django.contrib.auth import views as auth_views 

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path('accounts/login/', auth_views.LoginView.as_view(extra_context={'compact_header': True, 'hide_header_buttons': True}), name='login'),
    
    path('accounts/password_reset/', auth_views.PasswordResetView.as_view(template_name='core/password_reset_form.html'), name='password_reset'),
    path('accounts/password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='core/password_reset_done.html'), name='password_reset_done'),
    path('accounts/reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='core/password_reset_confirm.html'), name='password_reset_confirm'),
    path('accounts/reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='core/password_reset_complete.html'), name='password_reset_complete'),
    path('accounts/', include('django.contrib.auth.urls')),
    
    path('', views.home, name='home'), 

    path('cadastro/', views.cadastro, name='cadastro'),

    path('perfil/', views.perfil_view, name='perfil'),
    path('perfil/editar/', views.editar_dados, name='editar_dados'),
    path('perfil/favoritos/', views.favoritos_view, name='favoritos'),
    path('perfil/preferencias/', views.preferencias_view, name='preferencias'),

    path('eventos/', views.lista_eventos, name='lista_eventos'),
    path('eventos/buscar/', views.buscar_eventos, name='buscar_eventos'),
    path('eventos/resultado/', views.resultado_busca, name='resultado_busca'),
    path('evento/<int:evento_id>/', views.detalhe_evento, name='detalhe_evento'),
    path('evento/<int:evento_id>/toggle_favorito/', views.toggle_favorito, name='toggle_favorito'),
    path('evento/<int:evento_id>/avaliar/', views.avaliar_evento, name='avaliar_evento'),
    path('evento/<int:evento_id>/comentar/', views.adicionar_comentario, name='adicionar_comentario'),
    path('comentario/<int:comentario_id>/deletar/', views.deletar_comentario, name='deletar_comentario'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)