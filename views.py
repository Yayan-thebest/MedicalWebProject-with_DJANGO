from django.shortcuts import render, redirect, get_object_or_404

from .models import *
from .forms import *

# pour gerer les messages a afficher sur les views
from django.contrib import messages

  
from django.shortcuts import render, redirect 
from django.http import HttpResponse , JsonResponse
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth import authenticate, login, logout

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from .decorators import *
from django.views.decorators.csrf import csrf_protect

from django.db.models import Q # permet d'utiliser OR dans une requete

#import pour les messages automatiques
from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string # permet de lire le html qui sera ecrit dans temail_template


import json
import requests 


def pageAcceuil(request):
	return render(request, 'index.html')

def pageAbout(request):
	return render(request, 'about.html')

def pageService(request):
	return render(request, 'service.html')

def pageContact(request):
	return render(request, 'contact.html')

def dashboardPatient(request):
	return render(request, 'dashboardPatient.html')

def prendreRendezvous(request):
	return render(request, 'prendreRendezvous.html')


@csrf_protect
@unauthenticated_user
def registration_view(request):
	
	context = {}
	if request.POST:
		form = RegistrationForm(request.POST or None)
		if form.is_valid():
			user = form.save()
			nom = form.cleaned_data.get('nom')
			prenom = form.cleaned_data.get('prenom')
			email = form.cleaned_data.get('email')

			
			# on associe un user directement au group patient lorsqu'il cree un compte
			group = Group.objects.get(name='Patient')
			user.groups.add(group)

			# on associe un ser directement à un compte lorsqu'il cree un compte
			Account.objects.create(
				user=user,
			)

			print ('USER', user)

			messages.success(request, f'Compte créer avec succès pour : {prenom}')

			# apres l'inscription on connecte directement l'user
			#account = authenticate(email=email, password=raw_password)
			#login(request, account)
			return redirect('login')
		else:
			context['registration_form'] = form
	else :
		form = RegistrationForm(request.GET or None)
		context['registration_form'] = form
	return render(request, 'register.html', context)

@csrf_protect
@unauthenticated_user
def loginPage(request):
	user = request.user
	# si l'user est connecter on veut pas qu'il soit sur le login screen
	if user.is_authenticated:
		return redirect('acceuil')

	if request.POST:
		form = AccountAuthenticationForm(request.POST or None)
		if form.is_valid():
			email = request.POST['email']
			password = request.POST['password']
			user = authenticate(email=email, password=password)

			# si le compte user existe on redirige vers la page. Sinon on affiche msg d'erreur
			if user:
				login(request, user)


				template = render_to_string('email_template.html', {'patient': email})

				email = EmailMessage(
					'Merci de nous avoir contacter',
					template,
					settings.EMAIL_HOST_USER,
					[email],
					)
				email.fail_silently=False
				email.send()
				print(email)

				# condition pour rediriger l'user vers la page sur laquelle il veut se rendre. Apres s'etre connecter
				if'next' in request.POST:
					return redirect(request.POST.get('next'))
				else:
					return redirect('patient')
			else:
				messages.info(request, "Nom d'utilisateur ou mot de passe invalide")

	# sinon il sont sur la page login mais l'user ne c'est pas connecter
	else:
		form = AccountAuthenticationForm(request.GET or None)
	context ={
		'login_form' : form,		
	}
	return render(request, 'login.html', context)

@unauthenticated_user
def loginDocteur(request):
	user = request.user
	# si l'user est connecter on veut pas qu'il soit sur le login screen
	if user.is_authenticated:
		return redirect('acceuil')

	if request.POST:
		form = DocteurAuthenticationForm(request.POST or None)
		if form.is_valid():
			email = request.POST['email']
			password = request.POST['password']
			user = authenticate(email=email, password=password)

			# si le compte user existe on redirige vers la page
			if user:
				login(request, user)
				return redirect('docteur')
			else:
				messages.info(request, "Nom d'utilisateur ou mot de passe invalide")

	# sinon il sont sur la page login mais l'user ne c'est pas connecter
	else:
		form = DocteurAuthenticationForm(request.GET or None)
	context ={
		'login_form' : form,		
	}
	return render(request, 'loginDocteur.html', context)


def account_view(request):
	if not request.user.is_authenticated:
		return redirect ("login")	
	if request.POST:
		form = AccountUpdateForm(request.POST, instance=request.user)
		if form.is_valid():
			form.save()
	else:
		form = AccountUpdateForm (
				initial = {
					"email": request.user.email,
					"username": request.user.username,
				}
			)
	context = {
	'account_form': form,
	}

	return render(request, 'account.html/', context)


	
@login_required(login_url='login')
@allowed_users(allowed_roles=['Admin'])
def patientPage(request):
	user = request.user

	if not request.user.is_authenticated:
		return redirect ("login")

	if request.POST:
		form = AccountUpdateForm(request.POST or None, instance=request.user)
		if form.is_valid():
			# pour afficher les infos dans les texte box du form
			form.initial = {
				"email": request.POST['email'],
				"tel": request.POST['tel'],
				"adresse": request.POST['adresse'],
				}
			form.save()
			#return redirect('patient')
			#update_success = 'Informations Mise à jour avec succès!'
			messages.success(request, f'Informations mis à jour avec succès')
	else:
		form = AccountUpdateForm (
				initial = {
					"email": request.user.email,
					"tel": request.user.tel,
					"adresse": request.user.adresse,
				}
			)
	#-----------------Affichage Historique Rdv-----------------------
	historiqueRdvPatient = Rendezvous.objects.filter(identifiant=user.id)
	h = Rendezvous.objects.all()
	#-----------------------------------------------------

	#------------------------Filtre Rdv-----------------------
	searchBar_query = request.GET.get('searchBarPatient')
	print(searchBar_query)
	#icontains : case sensitive & contains : pas case sensitive, i : pour sensitive
	if searchBar_query != '' and searchBar_query is not None:
		historiqueRdvPatient = historiqueRdvPatient.filter(Q(consultation__contains=searchBar_query)
								 | Q(patient__contains=searchBar_query)
								 | Q(identifiant__contains=searchBar_query)
								 | Q(id__contains=searchBar_query)
								 | Q(aPayer__contains=searchBar_query)
								 | Q(statutRdv__iexact=searchBar_query)
								 ).distinct()
	


	context= {
		'account_form' : form,
		'historiqueRdvPatient': historiqueRdvPatient,
		'h':h,

		#'cons': cons,
		 
	} 
	return render(request, 'patient.html', context)


# Requete pour voir les details produits
def historique_detail(request, pk):
	patient = Rendezvous.objects.get(id=pk)
	print(patient.consultation)
	context = {
		"patient": patient,
	}
	return render(request, 'patient.html', context)

def modifierRdvPatient(request, pk):
	query_modifierRdv= Rendezvous.objects.get(pk=pk)
	if request.POST :
		formModifierRdvPatient = ModifierRdvPatientForm(request.POST or None, instance=query_modifierRdv)
		if formModifierRdvPatient.is_valid():
			formModifierRdvPatient.save()
			
	else:
		formModifierRdvPatient = ModifierRdvPatientForm ()
	context = {
		'query_modifierRdv': query_modifierRdv,
		'formModifierRdvPatient': formModifierRdvPatient,
	}
	return render(request, 'modifierMonRdv.html', context)



#---------------------Func pour la gestion des RDv par l'Admin---------------------------------
@login_required(login_url='login')
@allowed_users(allowed_roles=['Admin']) # seul les patient sont autorisé à voir cette page
#@admin_only
def gestionRdv(request):
	user = request.user
	empty=''

	if not request.user.is_authenticated:
		return redirect ("login")

	#-----------------Affichage Rdv-----------------------
	queryRdv = Rendezvous.objects.all()
	rdvTotal = queryRdv.count()

	queryRdvEnTraitement = Rendezvous.objects.filter(statutRdv='En traitement')
	rdvTotalEnTraitement = queryRdvEnTraitement.count()

	queryRdvConfirmer = Rendezvous.objects.filter(statutRdv='Confirmer')
	rdvTotalConfirmer = queryRdvConfirmer.count()
	#queryRdv = Rendezvous.objects.all()
	print(queryRdv)	
	consultation = Consultation.objects.all()
	#-----------------------------------------------------

	#-----------------Filtre Rdv-----------------------
	searchBar_query = request.GET.get('searchBarGestionRdv')
	print(searchBar_query)
	#icontains : case sensitive & contains : pas case sensitive, i : pour sensitive
	if searchBar_query != '' and searchBar_query is not None:
		queryRdv = queryRdv.filter(Q(consultation__contains=searchBar_query)
								 | Q(patient__contains=searchBar_query)
								 | Q(identifiant__contains=searchBar_query)
								 | Q(id__contains=searchBar_query)
								 | Q(aPayer__contains=searchBar_query)
								 | Q(statutRdv__iexact=searchBar_query)
								 ).distinct()	
	
	#-----------------------------------------------------
	context= {
		'queryRdv': queryRdv,
		'empty': empty,
		'rdvTotal': rdvTotal,
		'rdvTotalEnTraitement': rdvTotalEnTraitement,
		'rdvTotalConfirmer': rdvTotalConfirmer
	} 
	return render(request, 'gestionnaireRdv.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['Admin']) # seul les patient sont autorisé à voir cette page
def confirmerRdv(request, pk, patientId):
	user = request.user
	queryRdvInfoPatient = Rendezvous.objects.get(pk=pk)
	queryInfoPatient = Account.objects.get(pk=patientId)

	historiqueRdvPatient = Rendezvous.objects.filter(identifiant=patientId)

	
	form = ConfirmerRdvForm(request.POST or None, instance=queryRdvInfoPatient)
	if request.method == 'POST':
		if form.is_valid():

			form.save()
			#messages.success(request, "Rendez-Vous confirmer avec Succès. " )
			return  redirect('gestionRdv')


	context = {
		"title": 'Gestion Rendez-Vous #' + str(queryRdvInfoPatient.id) ,
		"queryRdvInfoPatient": queryRdvInfoPatient,
		"form": form,
		"username": 'Gérer par: ' + str(request.user),
		"queryInfoPatient": queryInfoPatient,
		'historiqueRdvPatient':historiqueRdvPatient,
	}
	return render(request, 'confirmerRdv.html', context)

def gestionRessourcePage(request):
	formCreateDocteur = CreeNouveauDocteur(request.POST or None)
	if formCreateDocteur.is_valid():
		formCreateDocteur.save()
		messages.success(request, 'Docteur ajouté avec succès' or None)
		return  redirect('gestionRessource')


	formCreatePost = CreeNouveauPost(request.POST or None)
	if formCreatePost.is_valid():
		formCreatePost.save()
		messages.success(request, 'Post ajouté avec succès' or None)
		return  redirect('gestionRessource')

	formCreateHoraireRdv = CreeNouvelHoraireForm(request.POST or None)
	if formCreateHoraireRdv.is_valid():
		formCreateHoraireRdv.save()
		messages.success(request, 'Horaire créer avec succès')
		return  redirect('gestionRessource')


	query_listDocteur = Docteur.objects.all()
	
	context = {
		"formCreateDocteur": formCreateDocteur,
		'formCreatePost': formCreatePost,
		'formCreateHoraireRdv':formCreateHoraireRdv,
		'query_listDocteur': query_listDocteur,

	}
	return render(request, 'gestionnaireRessources.html', context)

def create_postDocteur(request):
	if request.is_ajax():
		post = request.POST.get('post')
		print('POST Sent', post)

		Post.objects.create(nomPost=post
								  )
		return JsonResponse({'created': True})
	return JsonResponse({'created': False}, safe=False)

def create_Docteur(request):
	if request.is_ajax():
		nomDocteur = request.POST.get('nomDocteur')
		prenomDocteur = request.POST.get('prenomDocteur')
		birthDocteur = request.POST.get('birthDocteur')
		sexeDocteur = request.POST.get('sexeDocteur')
		emailDocteur = request.POST.get('emailDocteur')
		telDocteur = request.POST.get('telDocteur')
		adresseDocteur = request.POST.get('adresseDocteur')
		postDocteur = request.POST.get('postDocteur')


		Docteur.objects.create(nomDocteur=nomDocteur,
			prenomDocteur=prenomDocteur,
			dateNaissance=birthDocteur,
			tel = telDocteur,
			email =emailDocteur,
			adresse = adresseDocteur,
			sexe=sexeDocteur,
			post=postDocteur)
		return JsonResponse({'created': True})
	return JsonResponse({'created': False}, safe=False)


def voirPostDocteur(request, pk):
	query_infoDocteur = Docteur.objects.all()
	query_docteur = Docteur.objects.get(id=pk)
	query_listPostDocteur = list(query_docteur.post.all())

	query_deleteDocteur= Docteur.objects.get(id=pk)
	if request.method == 'POST':
		query_deleteDocteur.delete()
		messages.success(request, "Dr. " + str(query_deleteDocteur.nomDocteur)+ " supprimé avec succès")
		return redirect('/gestionRessource')


	if request.POST:
		form = AccountUpdateDocteurForm(request.POST, instance=query_docteur)
		if form.is_valid():
			# pour afficher les infos dans les texte box du form
			form.initial = {
				"email": request.POST['email'],
				"tel": request.POST['tel'],
				"adresse": request.POST['adresse'],
				}
			form.save()
			#return redirect('patient')
			#update_success = 'Informations Mise à jour avec succès!'
			messages.success(request, f'Informations mis à jour avec succès')
	else:
		form = AccountUpdateDocteurForm (
				initial = {
					"email": query_docteur.tel,
					"tel": query_docteur.tel,
					"adresse": query_docteur.adresse,
				}
			)

	context = {
		'account_form' : form,
		'query_docteur': query_docteur,
		'query_listPostDocteur': list(query_listPostDocteur),
		'query_deleteDocteur': query_deleteDocteur,

	}
	return render(request, 'voirPostDocteur.html', context)

def updateDocteur(request,pk):
	query_infoDocteur = Docteur.objects.all()
	query_docteur = Docteur.objects.get(id=pk)
	query_listPostDocteur = list(query_docteur.post.all())

	if request.POST:
		form = AccountUpdateDocteurForm(request.POST, instance=query_docteur)
		if form.is_valid():
			# pour afficher les infos dans les texte box du form
			form.initial = {
				"email": request.POST['email'],
				"tel": request.POST['tel'],
				"adresse": request.POST['adresse'],
				}
			form.save()
			#return redirect('patient')
			#update_success = 'Informations Mise à jour avec succès!'
			messages.success(request, f'Informations mis à jour avec succès')
	else:
		form = AccountUpdateDocteurForm (
				initial = {
					"email": query_docteur.tel,
					"tel": query_docteur.tel,
					"adresse": query_docteur.adresse,
				}
			)

	context = {
		'account_form' : form,
		'query_docteur': query_docteur,
		

	}
	return render(request, 'voirPostDocteur.html', context)

# Requete pour supprimer un Docteur
def delete_docteur(request, pk):
	query_deleteDocteur= Docteur.objects.get(id=pk)
	if request.method == 'POST':
		query_deleteDocteur.delete()
		messages.success(request, "Dr. " + str(query_deleteDocteur.nomDocteur)+ " supprimé avec succès")
		return redirect('/gestionRessource')
	context = {
		'query_deleteDocteur': query_deleteDocteur,
	}
	return render(request, 'delete_docteur.html', context)


def logoutUser(request):
	logout(request)
	return redirect('login')
#--------------------------------Fin fun Gestionnaire-------------------------------------------------------------

#-----------------Paypal-------------
#def checkout(request, *args, **kwargs):
def checkout(request, pk):
	product = Consultation.objects.get(pk=pk)
	context = {'product':product}
	return

def payementComplete(request):
	body = json.loads(request.body)
	print('BODY', body['consultationId'])
	print('BODY2', body['horaire_paypal'])
	print('BODY3', body['email'])
	horaire_paypal =  body['horaire_paypal']
	consultation = request.POST.get('consultation')
	print("PAYEMENT", str(body['consultationId']))
	consultation_obj = Consultation.objects.get(nom=body['consultationId'])

	horaire_obj = HorairesConsultation.objects.get(horaire=body['horaire_paypal'], consultation__nom=body['consultationId'])

	user = request.user
	query = Account.objects.get(pk=user.id)
	print( query)
	nomPatient = query.nom
	prenomPatient = query.prenom
	nom = nomPatient + " " + prenomPatient
	dateNaissance = query.dateNaissance
	tel = query.tel
	sexe = query.sexe
	adresse = query.adresse
	print(nomPatient)	



	Rendezvous.objects.create(identifiant=user.id,
								  patient=nom,
								  consultation=consultation_obj,
								  horaireConsultation= horaire_obj,
								  dateNaissance = dateNaissance,
								  tel=tel,
								  sexe=sexe,
								  adresse=adresse,
								  aPayer='A payer',
								  )
	return JsonResponse('Payement résussie! ', safe=False)



def payementComplete_invite(request):
	body = json.loads(request.body)
	print('BODY', body['consultationId'])
	print('BODY2', body['horaire_paypal'])
	print('BODY3', body['emailSend'])
	horaire_paypal =  body['horaire_paypal']
	consultation = request.POST.get('consultation')
	print("PAYEMENT", str(body['consultationId']))
	consultation_obj = Consultation.objects.get(nom=body['consultationId'])

	horaire_obj = HorairesConsultation.objects.get(horaire=body['horaire_paypal'], consultation__nom=body['consultationId'])

	user = request.user
	query = Account.objects.get(pk=user.id)
	print( query)
	nomPatient = query.nom
	prenomPatient = query.prenom
	nom = nomPatient + " " + prenomPatient
	dateNaissance = query.dateNaissance
	tel = query.tel
	sexe = query.sexe
	adresse = query.adresse
	print(nomPatient)	

	

	Rendezvous.objects.create(
								  consultation=consultation_obj,
								  horaireConsultation= horaire_obj,
								  dateNaissance = dateNaissance,
								  tel=tel,
								  sexe=sexe,
								  adresse=adresse,
								  aPayer='A payer',
								  )
	return JsonResponse('Payement résussie! ', safe=False)

def get_json_consultation_data(request):
	qs_val = Consultation.objects.values()
	return JsonResponse({'data': list(qs_val)})


#func pour avoir le prix d'une consultation en focntion de la consultation
def get_json_prix_data(request, *args, **kwargs):
	selected_consultation = kwargs.get('consultation')
	obj_models = (Consultation.objects.get(nom=selected_consultation))
	prix = obj_models.prixConsultation

	query_cons = (Consultation.objects.get(nom=selected_consultation))
	print(prix)
	print(query_cons)

	context ={
		'prix' : prix,
		'query_cons': query_cons,
	}

	# Avec json sa retourne un ens de clé valeur : 
	# prix : représente la clé et c'est ca qu'on appel dans ajax pour acceder a la valeur
	# prix : c'est la valeur qu'on retourne
	#return render(request, 'patient.html', context)
	return JsonResponse({'prix': (prix)})


# ici sera lhoraire
def get_json_horaire_data(request, *args, **kwargs):
	selected_consultation = kwargs.get('consultation')
	obj_models = list(HorairesConsultation.objects.filter(consultation__nom=selected_consultation).values())

	print(obj_models)
	return JsonResponse({'data': list(obj_models)})

# func qui permet de creer un rdv sans payement
def create_rdv(request):
	if request.is_ajax():
		consultation = request.POST.get('consultation')
		consultation_obj = Consultation.objects.get(nom=consultation)
		print(consultation)

		horaire = request.POST.get('horaire')

		# on ajoute car__name=car_obj.name pour eviter les conflicts entre deux donné
		# similaire par ex meme horaire pour 2 consultation ifferentes

		# consultation__nom = c'est la relation entre l'attribut de a table HoraireCons et la table consultation
		# car il ya une relation entre les deux tables avec la foreignKey
		horaire_obj = HorairesConsultation.objects.get(horaire=horaire, consultation__nom=consultation_obj.nom)
		print(horaire)

		patient = request.POST.get('patient')
		print(patient)

		user = request.user
		query = Account.objects.get(pk=user.id)
		print( query)
		nomPatient = query.nom
		prenomPatient = query.prenom
		nom = nomPatient + " " + prenomPatient
		dateNaissance = query.dateNaissance
		tel = query.tel
		sexe = query.sexe
		adresse = query.adresse
		print(nomPatient)

		#query1 = Patient.objects.filter(user__username='admin').values()
		#query1 = Patient.objects.get(user__username='admin')
		#print( query1.user.patient)

		Rendezvous.objects.create(identifiant=user.id,
								  patient=nom,
								  consultation=consultation_obj,
								  horaireConsultation=horaire_obj,
								  dateNaissance = dateNaissance,
								  tel=tel,
								  sexe=sexe,
								  adresse=adresse,
								  aPayer='Doit payer',
								  )
		

		return JsonResponse({'created': True})

	return JsonResponse({'created': False}, safe=False)



# func qui permet de creer un rdv sans payement
def create_rdv_invite(request):
	if request.is_ajax():
		consultation = request.POST.get('consultation')
		consultation_obj = Consultation.objects.get(nom=consultation)
		print(consultation)

		horaire = request.POST.get('horaire')
		email = request.POST.get('email')
		nomP = request.POST.get('nomPatient')


		#query1 = Patient.objects.filter(user__username='admin').values()
		#query1 = Patient.objects.get(user__username='admin')
		#print( query1.user.patient)

		Rendezvous.objects.create(
								  patient=nom,
								  consultation=consultation_obj,
								  horaireConsultation=horaire_obj,

								  aPayer='Doit payer',
								  )
		template = render_to_string('templates/email_template.html', {'patient': nomP})

		email = EmailMessage(
			'Merci de nous avoir contacter',
			template,
			settings.EMAIL_HOST_USER,
			[email],
			)
		email.fail_silently=False
		email.send()
		print(email)

		return JsonResponse({'created': True})
	return JsonResponse({'created': False}, safe=False)


# func qui permet de creer un rdv sans payement
def update_rdv(request,pk):
	if request.is_ajax():
		query_rdvUpdate = Rendezvous.objects.get(pk=pk)
		horaire = request.POST.get('horaire')

		horaire_obj = HorairesConsultation.objects.get(horaire=horaire)

		Rendezvous.objects.filter(pk = pk).update(horaireConsultation = horaire_obj,
												 heure='-------',
												 statutRdv='En traitement',
												 avecDocteur =None)
		return JsonResponse({'created': True})
	return JsonResponse({'created': False}, safe=False)

# func qui permet de creer un rdv sans payement
def annuler_rdv(request,pk):
	if request.is_ajax():

		Rendezvous.objects.filter(pk = pk).update(heure='-------',
												 statutRdv='Annuler',
												 avecDocteur =None)
		return redirect('/patient')
		#return JsonResponse({'created Annuler': True})
	return JsonResponse({'created': False}, safe=False)













#----------------------------- Pas utiliser-------------------
def contact(request):
	return render(request, 'contact.html')


#@allowed_users(allowed_roles=['docteur']) # seul les patient sont autorisé à voir cette page
def docteurPage(request):
	context = {
		"formAjouterPatient": "docteur",
		"title": "Ajouter un nouveau patient",
	}
	return render(request, 'docteur.html', context)

def get_json_rdvConfirm_data(request):
	qs_val = Rendezvous.objects.values()
	return JsonResponse({'data': list(qs_val)})

def get_json_heureRdvConfirm_data(request, *args, **kwargs):
	selected_consultation = kwargs.get('consultation')
	obj_models = list(Rendezvous.objects.values())
	print('test---- '+ str(obj_models))
	if selected_consultation == 'Confirmer':
		print('test***** ' +'OK')
	else:
		print("ERRORRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRR")
	#print('LISTE------' +str(obj_models.identifiant))
	return JsonResponse({'data': list(obj_models)})



# Create your views here.
@unauthenticated_user
def registerPage(request):
	'''
	form = CreatePatientForm()
	if request.method == 'POST':
		form = CreatePatientForm(request.POST)
		if form.is_valid():
			user = form.save()
			b = form.cleaned_data.get('username')# on recupere le nom d'user

			# on ajoute directly l'user dans le groupe patient lorqsu'il s'enregistre
			group = Group.objects.get(name='patient') 
			user.groups.add(group)

			# on cree un profil utilisateur
			Patient.objects.create(
				user=user,
			)

			messages.success(request,'Compte créer ' + b)
			return redirect('login') # si l'user s'inscrit on le redirige vers la page de login

	context = {'form':form}
	return render(request, 'register.html', context)
	'''
	'''
	context = {}
	if request.POST:
		form = RegistrationForm(request.POST)
		if form.is_valid():
			form.save()
			email = form.cleaned_data.get('email')
			raw_password = form.cleaned_data.get('password1')
			account = authenticate(email=email, password=raw_password)
			login(request, account)
			return redirect('login')
		else:
			context['registration_form'] = form
	else :
		form = RegistrationForm(request.GET)
		context['registration_form'] = form
	return render(request, 'register.html', context)
'''


'''
@unauthenticated_user
def loginPage(request):
	if request.method =='POST':
		username = request.POST.get('username')
		password = request.POST.get('password')

		user = authenticate(request, username=username, password=password)
		if user is not None:
			login(request, user)
			return redirect('home') # on redirige l'user a cette page quand il se connecte
		else:
			messages.info(request, "Nom d'utilisateur ou mot de passe invalide")

	context = {}
	return render(request, 'login.html', context)
'''