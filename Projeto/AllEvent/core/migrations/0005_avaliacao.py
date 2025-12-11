import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0004_categoria_evento_categoria"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Avaliacao",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "nota",
                    models.IntegerField(
                        validators=[
                            django.core.validators.MinValueValidator(1),
                            django.core.validators.MaxValueValidator(5),
                        ]
                    ),
                ),
                ("data_criacao", models.DateTimeField(auto_now_add=True)),
                (
                    "evento",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="avaliacoes",
                        to="core.evento",
                    ),
                ),
                (
                    "usuario",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "Avaliação",
                "verbose_name_plural": "Avaliações",
                "unique_together": {("evento", "usuario")},
            },
        ),
    ]
