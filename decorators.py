from django.http import HttpResponse
from django.shortcuts import redirect

# function qui permet de rediriger l'user ves la page de login si il n'est pas authentifier
# si il est authentifier et qu'il tente de retourner vers la page de login
# il sera toujours rediriger vers la page home
def unauthenticated_user(view_func):
	def wrapper_func(request, *args, **kwargs):
		# si l'user est authentifier on le redirige vers la page d'acceuil
		if request.user.is_authenticated:
			return redirect('patient')
		# sinon on le redirige vers la page de login
		else:
			return view_func(request, *args, **kwargs)

	return wrapper_func

# function qui permet de donner la permission à un user particulier 
# de voir une page spécifique
def allowed_users(allowed_roles=[]):
	def decorator(view_func):
		def wrapper_func(request, *args, **kwargs):			
			group = None
			if request.user.groups.exists():
				group = request.user.groups.all()[0].name
			if group in allowed_roles:
				return view_func(request, *args, **kwargs)
			else:
				return HttpResponse('Non autorisé à voir cette page.')
		return wrapper_func
	return decorator

# cette partie à revoir
def admin_only(view_func):
	def wrapper_func(request, *args, **kwargs):
		group = None
		if request.user.groups.exists():
			group = request.user.groups.all()[0].name
		if group == 'Patient':
			return redirect('acceuil')
		if group == 'Admin':
			return view_func(request, *args, **kwargs)

	return wrapper_func
	