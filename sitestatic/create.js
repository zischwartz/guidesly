var slide_api_url='/api/v1/slide/';
var staticel_api_url='/api/v1/staticelement/';

var file_api_url='/api/v1/userfile/';

// alert(current_slide_id);

// this should be better...

// console.log('hello world');
// var obj = jQuery.parseJSON('{"name":"John"}');
// alert( obj.name === "John" );

// add specific keys to mapping ko
// var slideMapping = {
// 	'children': {
// 		key: function(data) {
// 			return ko.utils.unwrapObservable(data.id);
// 		}
// 	}
// }


// // add flip
// 	$(".image_wrap").click(function(){
// 		$(this).flip({direction:'lr', speed: 150})
// 	});

// function StaticItem(file)
// {
// 	this.file= ko.observable(file);
// }



var slideViewModel;


// DOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOCREADDDDDDDDDDDDDDDDDDDYYYYYYYYYYYYYYYY
$(document).ready(function(){

	slideViewModel = ko.mapping.fromJS(initial_slide_json);

	slideViewModel.save =  function(formElelement){
					var jsonData = ko.toJSON(slideViewModel);
					$.ajax({
						url: slide_api_url+ current_slide_id + "/",
						type: "PUT",
						data:jsonData,
						success:function(data) { console.log(data); },
						contentType: "application/json",
						})};

	// ko.applyBindings(slideViewModel);
	// ko.applyBindings(slideViewModel, document.getElementById("#content"));
	
	// alert(slideViewModel.staticelements().length);

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


slideViewModel.media_files = ko.observableArray();


itemToAdd= new Object();
slideViewModel.add2slide = function() {
	// console.log("executed?");
	itemToAdd.file=this;
	itemToAdd.slide= slideViewModel.resource_uri();
	var jsonData = ko.toJSON(itemToAdd);
	$.ajax({
		url: staticel_api_url,
		type: "POST",
		data: jsonData,
		success:function(data) { console.log(data); },
		contentType: "application/json",
	});
	slideViewModel.media_files.remove(this);
	slideViewModel.staticelements.push(itemToAdd);

	// console.log(jsonData);

};

	
	
	
	
	// TODO, this requires processing to convert from userfile to staticelement. maybe make their models more similar? or not.
	// or maybe it should just add to the slide, first, and then reload the slide...
	// slideViewModel.staticelements.push(added);
	// console.log(this);
	// construct this:
// http://127.0.0.1:8000/api/v1/staticelement/2/?format=json
// {"autoplay": false, "display_title": false, "file": {"file": "/media/media/zbed.png", "id": "2", "slug": "zbed.png", "type": "image"}, "id": "2", "is_background": false, "is_primary": true, "length_minutes": null, "length_seconds": null, "resource_uri": "/api/v1/staticelement/2/", "slide": "/api/v1/slide/2/", "title": "", "type": "I"}
	





// pick image, video, audio or other.
$("#add_media_group h4").click(function(){
	media_type= $(this).data("media_type");
	$.getJSON(file_api_url + "?type="+media_type, function(data) {
		// $("#add_media_group h4").slideUp();
		for (x in  data.objects){slideViewModel.media_files.push(data.objects[x]);}
		});	
});




ko.applyBindings(slideViewModel);



// ko.applyBindings(slideViewModel);
// ko.applyBindings(toolViewModel);


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


