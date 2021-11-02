from django.contrib import admin
from .models import *

# permet de configuer l'ecran admin
from django.contrib.auth.admin import UserAdmin

# Register your models here.
#admin.site.register(Patient)
admin.site.register(ListDocteur)
admin.site.register(Post)
#admin.site.register(TypeConsultation)
#admin.site.register(ListConsultation)
#admin.site.register(HoraireDocteur)
admin.site.register(Rendezvous, AfficherID)
admin.site.register(HorairesConsultation)
admin.site.register(Consultation)


#admin.site.register(HoraireConsultation)

# class qui permet de designer la table Account 
class AccountAdmin(UserAdmin):
	# nom des attributs que l'on veut afficher
	list_display = ('email', 'nom', 'prenom' ,'date_joined', 'last_login', 'is_admin', 'is_staff', 'created_at', 'updated_at')
	# filtre de recherche
	search_fields = ('email', 'username',)
	# des valeurs qu'on ne doit jamais modifier
	readonly_fileds = ('date_joined', 'last_login')

	filter_horizontal = ()  
	list_filter = ()
	fieldsets = ()

admin.site.register(Account, AccountAdmin)

# class qui permet de designer la table Account 
class DocteurAdmin(UserAdmin):
	# nom des attributs que l'on veut afficher
	list_display = ('email', 'date_joined', 'last_login', 'is_admin', 'is_staff', )

	#list_display = ('email', 'username', 'date_joined', 'last_login', 'is_admin', 'is_staff')

	# filtre de recherche
	search_fields = ('email', 'username',)
	# des valeurs qu'on ne doit jamais modifier
	readonly_fileds = ('date_joined', 'last_login')

	filter_horizontal = ()  
	list_filter = ()
	fieldsets = ()

#admin.site.register(Docteur, DocteurAdmin)
class PostList(admin.ModelAdmin):
    list_display = ['nomDocteur', 'prenomDocteur', 'get_posts' ]

    def post(self, obj):
        return "\n".join([a.nomDocteur for a in obj.post.all()])
admin.site.register(Docteur, PostList)
