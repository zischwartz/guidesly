$(document).ready(function(){


$("#add_static").click(function(){
 $("#add_static_form").toggle('fast');
});


var current_el;
// Editing a Static Element, start by clicking on it in the preview
$(".a_static_element").click(function(e){
	element_id= $(this).data("id");
	current_el=  $(this);
	// $("#add_static_form").slideUp('fast');
	 $("#edit_static_form, #edit_static").slideDown('fast', function(e){
		// alert(element_id);
		$("#edit_static_form").load(current_url+"/editstatic/"+element_id);
		// put the url in a static variable thing in base.html
	});
})

//Deleting a static element
$(".delete_element_button").live('click', function(event){

	$(current_el).hide('fast', function(){$(this).remove();});

	$.ajax({
		url: $(this).attr('href'),
		type: 'DELETE',
		context: document.body,
		success: function(){
		$(this).addClass("done");}
	});
	 $("#edit_static_form, #edit_static").slideUp('fast');

	
 	event.preventDefault();
	return false;


})


}) // end docready