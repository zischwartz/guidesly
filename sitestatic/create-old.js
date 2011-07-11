

// cardViewModel.titleOrPlaceholder= ko.dependentObservable(function() {
//     if (this.title()!=="")
// 		{return this.title();}	
// 	else 
// 		{return 'Card Title (optional)';}
// }, cardViewModel);


// You're stupid. clone it, then programatically give it the data bind. Because it's just a data- attribute you dumbass. And then bend it.

// Give a form element focus
// and then detect when the .ue_editor's child loses focus and rever the flip.

//also just use the classes he built in

  // $("input:text:visible:first").focus();

$(".ue").live('click', function(){
	if ($(this).hasClass("ue_active"))
		{	
			$(this).removeClass("ue_active").revertFlip();
			return false;
		}
	//otherwise remove it from an element that already has it.	 And revert it?
	$('.ue_active').removeClass("ue_active").revertFlip();
	$(this).addClass("ue_active");
	$(this).flip({
		direction:'lr',
		speed: 150,
		// dontChangeColor: true,
		content: $(this).next('.ue_editor'),
		// onBefore: function(){ $(this).slideUp();}, //.data('bind', '');}
		onEnd: function(){ $(this).addClass("test");}//.data('bind', "value:title, valueUpdate: 'afterkeydown'"); ko.applyBindings(cardViewModel)}
		// onEnd: function(){ $(this).find("input:first").addClass("test").data('bind', "value:title, valueUpdate: 'afterkeydown'"); ko.applyBindings(cardViewModel)}
	});
	// alert($(this).addClass("test").html());
// $(this).next('.ue_editor').find("input:text:first").focus();

	// return false;
})

// $("#card_being_edited").click(function(){
// 	$('.ue_active').removeClass("ue_active").revertFlip();
// 	// $(this).addClass("ue_active");
// })


























// what a waste of time. i should not have spent to much time trying to make this work.


slideViewModel.add2slide = function() {
	// console.log("executed?");
	itemToAdd= new Object();
	itemToAdd = {
		file: {file:ko.observable(slideViewModel.media_files.remove(this)[0])},
		slide:  ko.observable(current_slide_id)
		};
	
	// itemToAdd.slide = ko.observable(current_slide_id);
	// slideViewModel.itemToAdd = ko.observable({file:slideViewModel.removedItem});
	slideViewModel.staticelements.push(itemToAdd);

	console.log(slideViewModel.staticelements())
	
	
	
	
	// TODO, this requires processing to convert from userfile to staticelement. maybe make their models more similar? or not.
	// or maybe it should just add to the slide, first, and then reload the slide...
	// slideViewModel.staticelements.push(added);
	// console.log(this);
	// construct this:
// http://127.0.0.1:8000/api/v1/staticelement/2/?format=json
// {"autoplay": false, "display_title": false, "file": {"file": "/media/media/zbed.png", "id": "2", "slug": "zbed.png", "type": "image"}, "id": "2", "is_background": false, "is_primary": true, "length_minutes": null, "length_seconds": null, "resource_uri": "/api/v1/staticelement/2/", "slide": "/api/v1/slide/2/", "title": "", "type": "I"}
	




// Directly below this is newer, but replaced by adding the json to the view

	// $.agetJSON(slide_api_url + current_slide_id + "/", function(data) {
	// 	// load initial data for the current slide.
	// 	slideViewModel = ko.mapping.fromJS(data);
	// 	ko.mapping.updateFromJS(slideViewModel, data);
	// 	//map it to ko
	// 	//and add a save function
	// 	slideViewModel.save =  function(formElelement){
	// 			var jsonData = ko.toJSON(slideViewModel);
	// 			$.ajax({
	// 				url: slide_api_url+ current_slide_id + "/",
	// 				type: "PUT",
	// 				data:jsonData,
	// 				success:function(data) { console.log(data); },
	// 				contentType: "application/json",
	// 				});
	// 			// alert('saved');
	// 			}; //end save function
	// 
	// 			//apply the bindings 
	// 		ko.applyBindings(slideViewModel);
	// 	
	// 		
	// 		// alert('The length of the array is ' + viewModel.staticelements().length);
	// 	});





$(document).ready(function(){

// console.log('hello world');

// $( "input[type=submit]").button();
// $( "button").button();





var icons = {header: "ui-icon-circle-arrow-e", headerSelected: "ui-icon-circle-arrow-s"};

$("#slide_element_toolbar").accordion({
	// header: '.top_button',
	autoHeight: false,
	collapsible: true,
	icons: icons,
	active: false
	// clearStyle: true,
});

$("#add_static_group").accordion({
	header: 'h4',
	autoHeight: false,
	collapsible: true,
	icons: icons,
	active: false
	// clearStyle: true,
}).bind('accordionchangestart', function(event, ui) {
	// alert(ui.newHeader.data('subtype'));
	subtype= ui.newHeader.data('subtype');
	$("."+subtype+"_chooser").load('/upload/list/'+subtype);
});


$(".choosefile").live("click", function(){
	static_el_id= $(this).addClass("selected").data('id');
	$(this).parent().parent().children(".see_all_button").slideDown();
	$(this).parent().children(".choosefile").not(this).slideUp();
	$(this).parent().next('form').find("input#id_file").val(static_el_id);
	$(this).parent().next('form').slideDown();
});

//this unselects
$(".see_all_button").click(function(){
	$(this).parent().find(".selected").removeClass("selected");
	$(this).next().children(".choosefile").slideDown();
	$(this).slideUp();
});



$("#add_interactive_group").accordion({
	header: 'h4',
	autoHeight: false,
	collapsible: true,
	icons: icons,
	active: false
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
});





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





}); // end docready


