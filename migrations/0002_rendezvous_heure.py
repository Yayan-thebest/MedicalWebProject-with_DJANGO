# Generated by Django 3.2 on 2021-06-30 23:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cliniquesb_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='rendezvous',
            name='heure',
            field=models.CharField(blank=True, choices=[('08:00', '08 AM'), ('08:30', '8:30'), ('09:00', '9:00'), ('09:30', '9 AM'), ('10:00', '10:00'), ('10:30', '10:30'), ('11:00', '11:00'), ('11:30', '11:30'), ('12:00', '12:00'), ('13:00', '13:00'), ('13:30', '13:30'), ('14:00', '14:00'), ('14:30', '14:30'), ('15:00', '15:00'), ('15:30', '15:30'), ('16:00', '16:00'), ('16:30', '16:30'), ('17:00', '17:00'), ('17:30', '17:30'), ('18:00', '18:00'), ('18:30', '18:30'), ('19:00', '19:00'), ('19:30', '19:30'), ('20:00', '20:00')], max_length=10, null=True),
        ),
    ]
