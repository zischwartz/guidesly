$(document).ready(function(){


$("#add_static").click(function(){
 $("#add_static_form").toggle('fast');
});


$(".a_static_element").click(function(e){
	element_id= $(this).data("id");
	 $("#add_static_form").slideDown('fast', function(e){
		// alert(element_id);
		$("#add_static_form").load(window.location+"/editstatic/"+element_id);
	});

})


}) // end docready