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


// DOOOOCCCCCCCCCCCCCCCRRRRRRRRREEEEEEEEEADDDDDDDDDDDDDDDDDDDYYYYYYYYYYYYYYYY
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

jQuery.easing.def = "easeOutQuart";


// var icons = {header: "ui-icon-circle-arrow-e", headerSelected: "ui-icon-circle-arrow-s"};
// var icons = {secondary: "photoIcon", headerSelected: "ui-icon-circle-arrow-s"};
$("#card_element_toolbar").accordion({
	autoHeight: false,
	collapsible: true,
	// icons: icons,
	active: false,
});

$(".uibutton").button();


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


	
	
	


cardViewModel.media_type= ko.observable("Media");

cardViewModel.changeMediaType= function(event){
	// alert($(event.currentTarget).data("media_type"));
	cardViewModel.media_type($(event.currentTarget).data("media_type"));
	// ko.applyBindings(cardViewModel);

}
cardViewModel.changeMediaTypeBack= function(event){
	cardViewModel.media_type("Media")
	// ko.applyBindings(cardViewModel);

}


// pick image, video, audio or other.
$("#add_media_group h4, h3 img").click(function(){
	cardViewModel.media_type= $(this).data("media_type");
	$.getJSON(file_api_url + "?type="+cardViewModel.media_type, function(data) {
		$("#add_media_group h4").slideUp();
		for (x in  data.objects){cardViewModel.media_files.push(data.objects[x]);}
		});	
	ko.applyBindings(cardViewModel);
	
	// alert(cardViewModel.media_type);
});




ko.applyBindings(cardViewModel);



// ko.applyBindings(cardViewModel);



});// end docready




