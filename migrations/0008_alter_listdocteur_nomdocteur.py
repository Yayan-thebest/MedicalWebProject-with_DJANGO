# Generated by Django 3.2 on 2021-07-02 01:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cliniquesb_app', '0007_auto_20210701_1745'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listdocteur',
            name='nomDocteur',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cliniquesb_app.docteur'),
        ),
    ]
