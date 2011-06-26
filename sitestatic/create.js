

$(document).ready(function(){

// console.log('hello world');

// $( ".button_group .button").button();





var icons = {header: "ui-icon-circle-arrow-e", headerSelected: "ui-icon-circle-arrow-s"};

$("#slide_element_toolbar").accordion({
	// header: '.top_button',
	autoHeight: false,
	collapsible: true,
	icons: icons,
	active: false,
	// clearStyle: true,
});

$("#add_static_group").accordion({
	header: 'h4',
	autoHeight: false,
	collapsible: true,
	icons: icons,
	active: false,
	// clearStyle: true,
});

$("#add_interactive_group").accordion({
	header: 'h4',
	autoHeight: false,
	collapsible: true,
	icons: icons,
	active: false,
	// clearStyle: true,
});

// $( ".button_group" ).tabs();



$(".button_group .button").click(function(){
	// console.log($(this).parent().next('.button_form'));
	subtype= $(this).data("subtype");
	subtype = "add_"+subtype+"_form";
	console.log(subtype);
	
	$(this).nextAll('.button_form').slideDown('fast');
});


// Editing a Static Element, start by clicking on it in the preview
var current_el;

$(".an_element").live('click', function(event){
	element_id= $(this).data("id");
	element_title= $(this).data("title");
	current_el=  $(this);
	// console.log(current_el);
	
	//  is the editing toolbar already open?
	if(($("#slide_element_toolbar").accordion( "option", "active" ))!=2) //2 is the index of the Edit . TODO make this less fragile
	{
		$("#slide_element_toolbar").accordion("activate", "#edit_static");
	}
	
	if ($(this).hasClass("a_static_el"))
	{
		$("#edit_static_form").load(current_url+"/editstatic/"+element_id);	
		$("#edited_type").text("Media: "+element_title);
	}
	
	if ($(this).hasClass("an_interactive_el"))
	{
		$("#edit_static_form").load(current_url+"/editinteractive/"+element_id);	
		$("#edited_type").text("Interaction: "+element_title);

	}
	
	
	event.preventDefault();
	return false;
})





//Deleting a static element
$(".delete_element_button").live('click', function(event){

	$("#slide_element_toolbar").accordion("activate", false);

	$(current_el).hide('fast', function(){
		$(this).remove();
		$("#edit_static_form").html("Click on a media or interactive element on the slide. Then you can edit it here.");
	});

	$.ajax({
		url: $(this).attr('href'),
		type: 'DELETE',
		context: document.body,
		success: function(){
		$(this).addClass("done");}
	});
	
 	event.preventDefault();
	return false;
})





}) // end docready


