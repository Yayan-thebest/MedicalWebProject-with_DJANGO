$(document).ready(function(){

        $('.table').paging({limit:1}); 

/*on utilise datetimeinput comme nom de classe car le fichier forms.py & models.py on a utiliser
DateTimeField pour e champ de date*/
/* si on avait utiliser DateField sa serai dateinput pour la classe*/
	$(".datetimeinput").datepicker({changeYear: true, changeMonth:true, dateFormat:'yyyy-mm-dd'});

});