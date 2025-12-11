from django.db import models
from django.contrib.auth.models import User 
from django.core.validators import MinValueValidator, MaxValueValidator

class Categoria(models.Model):
    nome = models.CharField(max_length=100)

    def __str__(self):
        return self.nome

class Evento(models.Model):
    nome = models.CharField(max_length=200)
    local = models.CharField(max_length=200)
    data = models.DateTimeField('data do evento')
    descricao = models.TextField(blank=True)
    imagem = models.ImageField(upload_to='eventos_imagens/', null=True, blank=True)
    
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True, blank=True)

    favoritos = models.ManyToManyField(User, related_name='eventos_favoritos', blank=True)

    def __str__(self):
        return self.nome

class Avaliacao(models.Model):
    evento = models.ForeignKey(Evento, on_delete=models.CASCADE, related_name='avaliacoes')
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    nota = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    data_criacao = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('evento', 'usuario')

    def __str__(self):
        return f"{self.usuario.username} - {self.evento.nome}: {self.nota}"

class Comentario(models.Model):
    evento = models.ForeignKey(Evento, on_delete=models.CASCADE, related_name='comentarios')
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    texto = models.TextField()
    data_criacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comentário de {self.usuario.username} em {self.evento.nome}"

class Preferencia(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name='preferencias')
    receber_emails = models.BooleanField(default=True)
    cidade_padrao = models.CharField(max_length=100, blank=True, null=True)
    interesses = models.ManyToManyField(Categoria, blank=True)

    def __str__(self):
        return f"Preferências de {self.usuario.username}"