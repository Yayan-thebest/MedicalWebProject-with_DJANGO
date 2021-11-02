# Generated by Django 3.2 on 2021-07-09 05:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cliniquesb_app', '0009_auto_20210705_1943'),
    ]

    operations = [
        migrations.AddField(
            model_name='rendezvous',
            name='messages',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='rendezvous',
            name='avecDocteur',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='cliniquesb_app.docteur', verbose_name='Avec Docteur'),
        ),
    ]
