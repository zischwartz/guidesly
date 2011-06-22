

$(document).ready(function(){

console.log('hello world');

// $( ".button_group .button").button();

$('#fileupload').fileupload();

    $.getJSON($('#fileupload form').prop('action'), function (files) {
        var fu = $('#fileupload').data('fileupload');
        fu._adjustMaxNumberOfFiles(-files.length);
        fu._renderDownload(files)
            .appendTo($('#fileupload .files'))
            .fadeIn(function () {
                // Fix for IE7 and lower:
                $(this).show();
            });
    });

    // Open download dialogs via iframes,
    // to prevent aborting current uploads:
    $('#fileupload .files a:not([target^=_blank])').live('click', function (e) {
        e.preventDefault();
        $('<iframe style="display:none;"></iframe>')
            .prop('src', this.href)
            .appendTo('body');
    });




var icons = {header: "ui-icon-circle-arrow-e", headerSelected: "ui-icon-circle-arrow-s"};
$("#slide_element_toolbar").accordion({
	// header: '.top_button',
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

$( ".button_group" ).tabs();



$(".button_group .button").click(function(){
	// console.log($(this).parent().next('.button_form'));
	subtype= $(this).data("subtype");
	subtype = "add_"+subtype+"_form";
	console.log(subtype);
	
	$(this).nextAll('.button_form').slideDown('fast');
});


// Editing a Static Element, start by clicking on it in the preview
var current_el;
$(".a_static_element").click(function(e){
	element_id= $(this).data("id");
	current_el=  $(this);
	// console.log(current_el);
	
	if(($("#slide_element_toolbar").accordion( "option", "active" ))!=1) //1 is the index of the Edit Static...
	{
		$("#slide_element_toolbar").accordion("activate", "#edit_static");
	}
	
	$("#edit_static_form").load(current_url+"/editstatic/"+element_id);
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
	
	$("#slide_element_toolbar").accordion("activate", false);

 	event.preventDefault();
	return false;


})


}) // end docready


