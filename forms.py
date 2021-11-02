from django import forms
from .models import *
#*****Pour modifier le register form**********
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
#*********************************************
from django.contrib.auth import authenticate # pour login

from phone_field import PhoneField


# form pour inserer un produit
class CreatePatientForm(UserCreationForm):
	#tel = forms.PhoneField(blank=True, help_text='Contact phone number')
	first_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
	last_name = forms.CharField(max_length=100,  widget=forms.TextInput(attrs={'class': 'form-control'}))
	email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))

	class Meta:
		model = User
		#fields = ['username', 'first_name', 'last_name','email', 'password1', 'password2']
		fields = [ 'first_name', 'last_name','email', 'password1', 'password2']

class RegistrationForm(UserCreationForm):
	email = forms.EmailField(max_length=100, help_text='Obligatoire. Entrer un email valide')
	tel 	    = PhoneField(blank=True, help_text='Numéro de téléphone')


	class Meta:
		model = Account
		fields =("email", "nom", 'prenom', 'dateNaissance', 'sexe', 'tel', 'adresse', "password1", "password2")
		#fields =("email", "username", "nom", 'prenom', 'tel', 'adresse', "password1", "password2")


	def clean_email(self):
		if self.is_valid():
			email = self.cleaned_data['email']
			
			# si l'account exist 
			try:
				account = Account.objects.exclude(pk=self.instance.pk).get(email=email)
			# si sa n'existe pas on peut update l'email
			except Account.DoesNotExist:
				return email
			raise forms.ValidationError('Email "%s" exist dejà' % email)
	def clean_username(self):
		if self.is_valid():
			username = self.cleaned_data['username']
			
			# si l'account exist 
			try:
				account = Account.objects.exclude(pk=self.instance.pk).get(username=username)
			# si sa n'existe pas on peut update l'email
			except Account.DoesNotExist:
				return username
			raise forms.ValidationError('Nom utilisateur "%s" existe dejà.' % username)
	def clean_tel(self):
		if self.is_valid():
			tel = self.cleaned_data['tel']
			
			# si l'account exist 
			try:
				account = Account.objects.exclude(pk=self.instance.pk).get(tel=tel)
			# si sa n'existe pas on peut update l'email
			except Account.DoesNotExist:
				return tel
			raise forms.ValidationError('Numéro de téléphone "%s" existe dejà.' % tel)
	

			
			
			

# Login user
class AccountAuthenticationForm(forms.ModelForm):
	password = forms.CharField(label="Mot de passe", widget=forms.PasswordInput)

	class Meta:
		model = Account
		fields = ('email', 'password')

	# permet de verifier si les credentiels de l'user sont valides
	# fonction disponible lorsqu'on extend la class Model
	def clean(self):

		# slef represente form. On verifie que les donnee entrées sont valides
		if self.is_valid():
			# on reference cela dans le fichier html avec les attributs 'name'
			email = self.cleaned_data['email']
			password = self.cleaned_data['password']
			if not authenticate(email=email, password=password):
				raise forms.ValidationError("Email ou mot de passe invalide.")
'''	
class DocteurAuthenticationForm(forms.ModelForm):
	password = forms.CharField(label="Mot de passe", widget=forms.PasswordInput)

	class Meta:
		model = Docteur
		fields = ('email', 'password')

	# permet de verifier si les credentiels de l'user sont valides
	# fonction disponible lorsqu'on extend la class Model
	def clean(self):

		# slef represente form. On verifie que les donnee entrées sont valides
		if self.is_valid():
			# on reference cela dans le fichier html avec les attributs 'name'
			email = self.cleaned_data['email']
			password = self.cleaned_data['password']
			if not authenticate(email=email, password=password):
				raise forms.ValidationError("Email ou mot de passe invalide.")
	'''
class AccountUpdateForm(forms.ModelForm):
	class Meta:
		model = Account
		fields = ['email','tel','adresse']

	def clean_email(self):
		if self.is_valid():
			email = self.cleaned_data['email']
			
			# si l'account exist 
			try:
				account = Account.objects.exclude(pk=self.instance.pk).get(email=email)
			# si sa n'existe pas on peut update l'email
			except Account.DoesNotExist:
				return email
			raise forms.ValidationError('Email "%s" existe dejà.' % email)
	def clean_tel(self):
		if self.is_valid():
			tel = self.cleaned_data['tel']			
			# si l'account exist 
			try:
				account = Account.objects.exclude(pk=self.instance.pk).get(username=tel)
			# si sa n'existe pas on peut update l'email
			except Account.DoesNotExist:
				return tel
			raise forms.ValidationError('Numéro de téléphone "%s" existe dejà.' % tel)
	


	'''
class AccountUpdateForm(forms.ModelForm):
	class Meta:
		model = Account
		fields = ['email','username','tel','adresse']

	def clean_email(self):
		if self.is_valid():
			email = self.cleaned_data['email']
			
			# si l'account exist 
			try:
				account = Account.objects.exclude(pk=self.instance.pk).get(email=email)
			# si sa n'existe pas on peut update l'email
			except Account.DoesNotExist:
				return email
			raise forms.ValidationError('Email "%s" existe dejà.' % email)
	def clean_username(self):
		if self.is_valid():
			username = self.cleaned_data['username']
			
			# si l'account exist 
			try:
				account = Account.objects.exclude(pk=self.instance.pk).get(username=username)
			# si sa n'existe pas on peut update l'email
			except Account.DoesNotExist:
				return username
			raise forms.ValidationError('Nom utilisateur "%s" existe dejà.' % username)
	def clean_tel(self):
		if self.is_valid():
			tel = self.cleaned_data['tel']			
			# si l'account exist 
			try:
				account = Account.objects.exclude(pk=self.instance.pk).get(username=tel)
			# si sa n'existe pas on peut update l'email
			except Account.DoesNotExist:
				return tel
			raise forms.ValidationError('Numéro de téléphone "%s" existe dejà.' % tel)
'''	

# form pour effectuer des recherches a partir du nom de la consultation et date
class HistoriqueSearchForm(forms.ModelForm):
	class Meta:
		model = Rendezvous
		fields = ['consultation']

class ConfirmerRdvForm(forms.ModelForm):
	class Meta:
		model = Rendezvous
		fields = ['statutRdv', 'heure', 'avecDocteur']

class CreeNouvelHoraireForm(forms.ModelForm):
	class Meta:
		model = HorairesConsultation
		fields = '__all__'

class ModifierRdvPatientForm(forms.ModelForm):
	class Meta:
		model = Rendezvous
		fields = ['statutRdv', 'heure']

class CreeNouveauDocteur(forms.ModelForm):
	class Meta:
		model = Docteur
		fields = '__all__'
		
class CreeNouveauPost(forms.ModelForm):
	class Meta:
		model = Post
		fields = '__all__'

class AccountUpdateDocteurForm(forms.ModelForm):
	class Meta:
		model = Docteur
		fields = '__all__'