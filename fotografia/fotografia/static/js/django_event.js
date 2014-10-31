//modificar windows alert estilo css, la parte que dice seleccionaste dos fotos

//esto que esta comentado ignorar.............
//#####################################################################
//radio.each(function() {                                             #
//	nam = $(this).attr('name');                                       #
//	if ($('input:radio[name="'+nam+'"]:checked').val() === "S"){      #
//	numero++;                                                         #
//			}                                                         #
//	});                                                               #
//#####################################################################
(function($) {
$(document).ready(function(){

if($("album_form")){
	$( "#album_form" ).submit(function( e ) {
	radio=$("#album_form input[type='radio']")
	var numero=1;
	for(j=0;j<=radio.length -4;j++){
	nam = radio[j].getAttribute("name");
	if ($('input:radio[name="'+nam+'"]:checked').val() === "S"){
	numero++;}}
	if(numero <= 1){
	alert("no seleccionaste foto de portada");
	e.preventDefault();}
	else if (numero >3){
	alert("seleccionaste dos fotos de portada debes seleccionar solamente una");
	e.preventDefault();}
	else{
	return true;
	}
		});								
	  }
	});
})(django.jQuery);