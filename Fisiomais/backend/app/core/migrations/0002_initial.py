# Generated by Django 5.1.4 on 2025-01-02 20:03

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('core', '0001_initial'),
        ('usuarios', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='agendamento',
            name='cliente',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='agendamentos', to='usuarios.cliente'),
        ),
        migrations.AddField(
            model_name='agendamento',
            name='colaborador',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='agendamentos', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='colaboradoresservicos',
            name='colaborador',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='servicos_relacionados', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='horario',
            name='colaborador',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='horarios', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='colaboradoresservicos',
            name='servico',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='colaboradores_relacionados', to='core.servico'),
        ),
        migrations.AddField(
            model_name='agendamento',
            name='servico',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='agendamentos', to='core.servico'),
        ),
    ]