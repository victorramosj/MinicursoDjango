# Generated by Django 5.1.4 on 2025-01-02 21:04

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_initial'),
        ('usuarios', '0002_remove_cliente_email_remove_cliente_nome_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='agendamento',
            name='colaborador',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='agendamentos', to='usuarios.colaborador'),
        ),
        migrations.AlterField(
            model_name='colaboradoresservicos',
            name='colaborador',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='servicos_relacionados', to='usuarios.colaborador'),
        ),
        migrations.AlterField(
            model_name='horario',
            name='colaborador',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='horarios', to='usuarios.colaborador'),
        ),
    ]