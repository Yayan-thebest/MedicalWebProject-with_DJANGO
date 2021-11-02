# Generated by Django 3.2 on 2021-06-30 23:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Consultation',
            fields=[
                ('nom', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('prixConsultation', models.CharField(blank=True, max_length=50, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Docteur',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nomDocteur', models.CharField(blank=True, max_length=50, null=True)),
                ('prenomDocteur', models.CharField(blank=True, max_length=50, null=True)),
                ('dateNaissance', models.CharField(max_length=15, null=True)),
                ('sexe', models.CharField(blank=True, max_length=8, null=True)),
                ('tel', models.CharField(max_length=20)),
                ('adresse', models.CharField(blank=True, max_length=50, null=True)),
                ('post', models.CharField(blank=True, max_length=50, null=True)),
                ('salaire', models.IntegerField(blank=True, default='0', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='HorairesConsultation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('horaire', models.DateField(blank=True, null=True)),
                ('consultation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cliniquesb_app.consultation')),
            ],
        ),
        migrations.CreateModel(
            name='ListDocteur',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nomDocteur', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='cliniquesb_app.docteur')),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nomPost', models.CharField(blank=True, max_length=50, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='TypeConsultation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nomConsultation', models.CharField(blank=True, max_length=50, null=True)),
                ('prixConsultation', models.CharField(blank=True, max_length=50, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Rendezvous',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('identifiant', models.CharField(blank=True, max_length=100, null=True)),
                ('patient', models.CharField(blank=True, max_length=100, null=True)),
                ('consultation', models.CharField(blank=True, max_length=100, null=True)),
                ('dateNaissance', models.CharField(max_length=15, null=True)),
                ('tel', models.CharField(max_length=20, null=True)),
                ('sexe', models.CharField(blank=True, max_length=6, null=True)),
                ('adresse', models.CharField(blank=True, max_length=50, null=True)),
                ('date', models.DateTimeField(auto_now_add=True, verbose_name='date ')),
                ('aPayer', models.CharField(blank=True, max_length=50, null=True)),
                ('statutRdv', models.CharField(blank=True, choices=[('Confirmer', 'CONFIRMER'), ('Non Confirmer', 'NON CONFIRMER')], default='En traitement', max_length=14, null=True, verbose_name='Statut du rendez-vous')),
                ('avecDocteur', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='cliniquesb_app.listdocteur', verbose_name='Avec Docteur')),
                ('horaireConsultation', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='cliniquesb_app.horairesconsultation')),
            ],
        ),
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('email', models.EmailField(max_length=100, unique=True, verbose_name='email')),
                ('username', models.CharField(max_length=50, null=True, unique=True)),
                ('date_joined', models.DateTimeField(auto_now_add=True, verbose_name='date joined')),
                ('last_login', models.DateTimeField(auto_now=True, verbose_name='last login')),
                ('nom', models.CharField(max_length=100)),
                ('prenom', models.CharField(max_length=100)),
                ('dateNaissance', models.CharField(max_length=15, null=True)),
                ('tel', models.CharField(max_length=20)),
                ('sexe', models.CharField(blank=True, max_length=6, null=True)),
                ('adresse', models.CharField(blank=True, max_length=50, null=True)),
                ('is_admin', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_superuser', models.BooleanField(default=False)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
