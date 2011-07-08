var card_api_url='/api/v1/card/';
var staticel_api_url='/api/v1/staticelement/';

var file_api_url='/api/v1/userfile/';

// alert(current_card_id);

// this should be better...

// console.log('hello world');
// var obj = jQuery.parseJSON('{"name":"John"}');
// alert( obj.name === "John" );

// add specific keys to mapping ko
// var cardMapping = {
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



var cardViewModel;


// DOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOCREADDDDDDDDDDDDDDDDDDDYYYYYYYYYYYYYYYY
$(document).ready(function(){

	cardViewModel = ko.mapping.fromJS(initial_card_json);

	cardViewModel.save =  function(formElelement){
					var jsonData = ko.toJSON(cardViewModel);
					$.ajax({
						url: card_api_url+ current_card_id + "/",
						type: "PUT",
						data:jsonData,
						//success:function(data) { console.log(data); },
						contentType: "application/json",
						})};

	// ko.applyBindings(cardViewModel);
	// ko.applyBindings(cardViewModel, document.getElementById("#content"));
	
	// alert(cardViewModel.staticelements().length);

// Make the sidbar pretty, animated, acordian
// 
var icons = {header: "ui-icon-circle-arrow-e", headerSelected: "ui-icon-circle-arrow-s"};
$("#card_element_toolbar").accordion({
	// header: '.top_button',
	autoHeight: false,
	collapsible: true,
	icons: icons,
	active: false
});


cardViewModel.media_files = ko.observableArray();


itemToAdd= new Object();
cardViewModel.add2card = function() {

	// itemToAdd.file=this.resource_uri; //WOPRKS
	itemToAdd.file=this;
	
	itemToAdd.card= cardViewModel.resource_uri();
	var jsonData = ko.toJSON(itemToAdd);
	$.ajax({
		url: staticel_api_url,
		type: "POST",
		data: jsonData,
		success:function(data) { console.log(data); },
		contentType: "application/json",
	});
	cardViewModel.media_files.remove(this);
	// itemToAdd.file=this;                             //not present
	cardViewModel.staticelements.push(itemToAdd);



};

	
	
	
	
	// TODO, this requires processing to convert from userfile to staticelement. maybe make their models more similar? or not.
	// or maybe it should just add to the card, first, and then reload the card...
	// cardViewModel.staticelements.push(added);
	// console.log(this);
	// construct this:
// http://127.0.0.1:8000/api/v1/staticelement/2/?format=json
// {"autoplay": false, "display_title": false, "file": {"file": "/media/media/zbed.png", "id": "2", "slug": "zbed.png", "type": "image"}, "id": "2", "is_background": false, "is_primary": true, "length_minutes": null, "length_seconds": null, "resource_uri": "/api/v1/staticelement/2/", "card": "/api/v1/card/2/", "title": "", "type": "I"}
	





// pick image, video, audio or other.
$("#add_media_group h4").click(function(){
	media_type= $(this).data("media_type");
	$.getJSON(file_api_url + "?type="+media_type, function(data) {
		// $("#add_media_group h4").cardUp();
		for (x in  data.objects){cardViewModel.media_files.push(data.objects[x]);}
		});	
});




ko.applyBindings(cardViewModel);



// ko.applyBindings(cardViewModel);
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


