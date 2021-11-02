from django.db import models
from django.contrib import admin # pour utiliser le ID
from phone_field import PhoneField

from django.contrib.auth.models import AbstractUser, AbstractBaseUser, BaseUserManager, PermissionsMixin
#from django.contrib.auth.models import User
from django.conf import settings

from django.utils import formats

from datetime import datetime

from django.utils import timezone



class MyAccountMananger(BaseUserManager):
	# on ajoute les required fields et username_field
	def create_user(self, email, password=None):
		if not email :
			raise ValueError("Les utilisateurs doivent avoir un email")
		if not username :
			raise ValueError("Les utilisateurs doivent avoir un nom d'utilisateur")	
		#if not nom :
		#	raise ValueError("Les utilisateurs doivent avoir un nom d'utilisateur")			
		
		#
		user = self.model(
			   email = self.normalize_email(email), # met les caracs de l'emial en miniscule
			   #username = username,
			)
		user.set_password(password)
		user.save(using=self._db)
		return user

	def create_superuser(self, email, password):
		user = self.create_user(
			   email = self.normalize_email(email), # met les caracs de l'email en miniscule
			   password = password,
			  # username = username,
			)
		user.is_admin = True
		user.is_staff = True
		user.is_superuser = True
		user.save(using=self._db)
		return user



# Create your models here.
class Account(AbstractBaseUser, PermissionsMixin):
	#models.CASCADE permet de supprimer toute les nfos de l'user avec la table avec la quelle il a une relation
	user     	= models.OneToOneField('cliniquesb_app.Account', null=True, on_delete=models.CASCADE)
	email 		= models.EmailField(verbose_name="Email", max_length=100, unique=True)
	username 	= models.CharField(max_length=50, null=True, default='Null')
	date_joined = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
	last_login  = models.DateTimeField(verbose_name='last login', auto_now=True)
	nom 	    = models.CharField(max_length=100)
	prenom  	= models.CharField(max_length=100)
	dateNaissance  		= models.CharField(max_length=15, null=True)
	tel 		= models.CharField(max_length=20)
	sexe        = models.CharField(max_length=6, blank=True, null=True)
	adresse     = models.CharField(max_length=50, blank=True, null=True)
	is_admin 	= models.BooleanField(default=False)
	is_active   = models.BooleanField(default=True)
	is_staff 	= models.BooleanField(default=False)
	is_superuser = models.BooleanField(default=False)
#	dateCreationPatient   = models.DateField(auto_now_add=True) 
	created_at = models.DateTimeField(auto_now_add=True, null=True)
	updated_at = models.DateTimeField(auto_now=True, null=True)


	USERNAME_FIELD = 'email' # ce quon demande pour la connection
	REQUIRED_FIELDS = ['username',] #les champs bligatoire pour pouvoir creer un compte on peut ajouter ce qu'on veut

	objects = MyAccountMananger()

	def __str__(self):
		return self.email

	# obligatoire pour les customs user models
	def has_perm(self, perm, obj=None):
		return self.is_admin

	def has_module_perms(self, app_label):
		return True

class Post(models.Model):
	nomPost = models.CharField(verbose_name='Nom du post', max_length=50, null=True)

	def __str__(self): # permet d'afficher le nom des elements de la table dans djangoadmin
		return  f"{self.nomPost}"


class TypeConsultation(models.Model):
	nomConsultation = models.CharField(max_length=50, blank=True, null=True)
	prixConsultation = models.CharField(max_length=50, blank=True, null=True)

	def __str__(self): # permet d'afficher le nom des elements de la table dans djangoadmin
		return str(self.nomConsultation)


#------TEST-------------

class Docteur(models.Model):
	CHOIX_GENRE = (
	('M', 'M'),
	('F', 'F'),)
	nomDocteur = models.CharField(verbose_name='Nom', max_length=50, null=True)
	prenomDocteur = models.CharField(verbose_name='Prenom', max_length=50, null=True)
	dateNaissance  		= models.CharField(verbose_name='Date de naissance', max_length=15, null=True)
	sexe = models.CharField(choices=CHOIX_GENRE, max_length=1, null=True)
	tel 		= models.CharField(verbose_name='Téléphone', max_length=20, unique=True)
	email 		= models.EmailField(verbose_name="Email", max_length=100, blank=True, unique=True)
	adresse = models.CharField(max_length=50, blank=True, null=True)
	post = models.ManyToManyField(Post)
	salaire = models.IntegerField(default='0', blank=True, null=True)
	

	#func qui permet d'afficher list_display de l'attribut manyTomanyField
	def get_posts(self):
		return "\n".join([ f"{p}, "  for p in self.post.all()])

	def __str__(self): # permet d'afficher le nom des elements de la table dans djangoadmin
		return str(self.nomDocteur + " "+ self.prenomDocteur) + " ("+ "\n".join([ f"{p},"  for p in self.post.all()]) +")"

class ListDocteur(models.Model):
	nomDocteur = models.ForeignKey(Docteur, on_delete=models.CASCADE) # permet de supprimer tout les datas relier a une categorie
	def __str__(self): # permet d'afficher le nom des elements de la table dans djangoadmin
		return str(self.nomDocteur)

class Consultation(models.Model):
	nom = models.CharField(primary_key=True, max_length=50)	
	prixConsultation = models.CharField(max_length=50, blank=True, null=True)

	def __str__(self):
		#return f"{self.nom}-{self.prixConsultation}F"
		return f"{self.nom}"


class HorairesConsultation(models.Model):
	horaire   = models.DateField(blank=True,  null=True) 
	consultation = models.ForeignKey(Consultation, on_delete=models.CASCADE)
	
	def __str__(self):
		return f"{self.horaire}"

class AfficherID(admin.ModelAdmin):
	readonly_fields = ('id',)


class Rendezvous(models.Model):
	CHOIX_CONFIRMATION = (
	('Confirmer', 'CONFIRMER'),
	('Non Confirmer', 'NON CONFIRMER'),
	('Annuler', 'Annuler'),)
	CHOIX_HEURE =   (('08:00', '08 AM'),
					('08:30', '8:30'),
					('09:00', '9:00'),
					('09:30', '9 AM'),
					('10:00', '10:00'),
					('10:30', '10:30'),
					('11:00', '11:00'),
					('11:30', '11:30'),
					('12:00', '12:00'),
					('13:00', '13:00'),
					('13:30', '13:30'),
					('14:00', '14:00'),
					('14:30', '14:30'),
					('15:00', '15:00'),
					('15:30', '15:30'),
					('16:00', '16:00'),
					('16:30', '16:30'),
					('17:00', '17:00'),
					('17:30', '17:30'),
					('18:00', '18:00'),
					('18:30', '18:30'),
					('19:00', '19:00'),
					('19:30', '19:30'),
					('20:00', '20:00'), )
	identifiant = models.CharField(max_length=100, blank=True, null=True)
	patient = models.CharField(max_length=100, blank=True, null=True)
	consultation  =models.CharField(max_length=100, blank=True, null=True)
	#consultation  = models.ForeignKey(Consultation, on_delete=models.CASCADE)
	horaireConsultation  = models.ForeignKey(HorairesConsultation, on_delete=models.CASCADE, null=True)
	#date = models.DateField(verbose_name=("Horaire"), auto_now_add=True, null=True)
	dateNaissance  		= models.CharField(max_length=15, null=True)
	tel 		= models.CharField(max_length=20, null=True)
	sexe        = models.CharField(max_length=6, blank=True, null=True)
	adresse     = models.CharField(max_length=50, blank=True, null=True)
	date   		= models.DateTimeField(verbose_name='date ', auto_now_add=True)
	aPayer 		= models.CharField(max_length=50, blank=True, null=True)
	statutRdv 	= models.CharField(verbose_name='Statut du rendez-vous', max_length=14, blank=True, null=True, choices=CHOIX_CONFIRMATION, default="En traitement")
	#messages 	= models.CharField(max_length=500, blank=True, null=True)
	heure =  models.CharField(max_length=10, blank=True, choices=CHOIX_HEURE, null=True)
	avecDocteur =  models.ForeignKey(Docteur, verbose_name='Avec Docteur', on_delete=models.CASCADE, blank=True, null=True)




	def __str__(self):
		return  f"{self.identifiant} - {self.patient} - {self.consultation}"
# ajouter date de creation

