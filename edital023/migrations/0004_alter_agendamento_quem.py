# Generated by Django 3.2.3 on 2021-05-29 02:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('edital023', '0003_agendamento'),
    ]

    operations = [
        migrations.AlterField(
            model_name='agendamento',
            name='quem',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='edital023.cidadao', unique=True, verbose_name='Cidadão'),
        ),
    ]
