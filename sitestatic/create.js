var slide_api_url='/api/v1/slide/';
var file_api_url='/api/v1/userfile/';
// alert(current_slide_id);

// this should be better...

// console.log('hello world');
// var obj = jQuery.parseJSON('{"name":"John"}');
// alert( obj.name === "John" );

// add keys
// var slideMapping = {
// 	'children': {
// 		key: function(data) {
// 			return ko.utils.unwrapObservable(data.id);
// 		}
// 	}
// }


// add flip
	// $(".slide_title").click(function(){
	// 	$(this).flip({direction:'lr', speed: 150})
	// });

var viewModel = {};

$(document).ready(function(){


	$.getJSON(slide_api_url + current_slide_id + "/", function(data) {
			viewModel = ko.mapping.fromJS(data);
			ko.applyBindings(viewModel);	
			// alert('The length of the array is ' + viewModel.staticelements().length);
		});




// Make the sidbar pretty, animated, acordian
// 
var icons = {header: "ui-icon-circle-arrow-e", headerSelected: "ui-icon-circle-arrow-s"};

$("#slide_element_toolbar").accordion({
	// header: '.top_button',
	autoHeight: false,
	collapsible: true,
	icons: icons,
	active: false

});

$("#add_media_group h4").click(function(){
	media_type= $(this).data("media_type");
	// alert(media_type);
	$.getJSON(file_api_url, function(data) {
			viewModel.media_files += ko.mapping.fromJS(data);
			ko.applyBindings(viewModel);
			});	
	$("#add_media_group h4").slideUp();
});


// $("#add_static_group").accordion({
// 	header: 'h4',
// 	autoHeight: false,
// 	collapsible: true,
// 	icons: icons,
// 	active: false
// 	// clearStyle: true,
// });
// 
// 
// 
// $("#add_interactive_group").accordion({
// 	header: 'h4',
// 	autoHeight: false,
// 	collapsible: true,
// 	icons: icons,
// 	active: false
// 	// clearStyle: true,
// });


});// end docready




// 
// 
// $("#add_static_group").accordion({
// 	header: 'h4',
// 	autoHeight: false,
// 	collapsible: true,
// 	icons: icons,
// 	active: false
// 	// clearStyle: true,
// }).bind('accordionchangestart', function(event, ui) {
// 	// alert(ui.newHeader.data('subtype'));
// 	subtype= ui.newHeader.data('subtype');
// 	// $("."+subtype+"_chooser").load('/upload/list/'+subtype);
// });
// 
// $("#add_interactive_group").accordion({
// 	header: 'h4',
// 	autoHeight: false,
// 	collapsible: true,
// 	icons: icons,
// 	active: false
// 	// clearStyle: true,
// });


