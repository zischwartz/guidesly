

$(document).ready(function(){

// console.log('hello world');

$( "input[type=submit]").button();
$( "button").button();





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
}).bind('accordionchangestart', function(event, ui) {
	// alert(ui.newHeader.data('subtype'));
	subtype= ui.newHeader.data('subtype')
	$("."+subtype+"_chooser").load('/upload/list/'+subtype);
});

$(".choosefile").live("click", function(){
	static_el_id= $(this).addClass("selected").data('id');
	$(this).parent().parent().children(".see_all_button").slideDown();
	$(this).parent().children(".choosefile").not(this).slideUp()
	$(this).parent().next('form').find("input#id_file").val(static_el_id);
	$(this).parent().next('form').slideDown();
});

//this unselects
$(".see_all_button").click(function(){
	$(this).parent().find(".selected").removeClass("selected");
	$(this).next().children(".choosefile").slideDown()
	$(this).slideUp();
});

$("#add_interactive_group").accordion({
	header: 'h4',
	autoHeight: false,
	collapsible: true,
	icons: icons,
	active: false,
	// clearStyle: true,
});



// var active = $( "#add_static_group" ).accordion( "option", "active" );
 // alert(active);

// 
// $(".button_group .button").click(function(){
// 	// console.log($(this).parent().next('.button_form'));
// 	subtype= $(this).data("subtype");
// 	subtype = "add_"+subtype+"_form";
// 	// console.log(subtype);
// 	
// 	$(this).nextAll('.button_form').slideDown('fast');
// });


// Editing an Element, start by clicking on it in the preview
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





//Deleting an element
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


