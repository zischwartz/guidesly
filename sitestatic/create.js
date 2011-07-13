var card_api_url='/api/v1/card/';
var staticel_api_url='/api/v1/staticelement/';
var file_api_url='/api/v1/userfile/';

var cardViewModel;
var converter = new Showdown.converter();

var initial_card_object;
var mapping;

// DOOOOCCCCCCCCCCCCCCCRRRRRRRRREEEEEEEEEADDDDDDDDDDDDDDDDDDDYYYYYYYYYYYYYYYY
$(document).ready(function(){	
	
	$(".uibutton").button();

	mapping = {
	    'staticelements': {
	        key: function(data) {
				// console.log('mapping key:');
				// console.log(data.resource_uri);
	            // return fake.resource_uri;
	            return ko.utils.unwrapObservable(data.resource_uri);
	        }
	    }
	}


	// cardViewModel = ko.mapping.fromJSON(initial_card_json, mapping);
	// console.log(initial_card_json);
	initial_card_object= jQuery.parseJSON(initial_card_json);
	cardViewModel = ko.mapping.fromJS(initial_card_object, mapping);
	// or
	// cardViewModel = ko.mapping.fromJSON(initial_card_json, mapping);
	// console.log(initial_card_object);

	// cardViewModel.staticelements.mappedRemove({ resource_uri : '/api/v1/staticelement/4/' });
	//this line works, so the mapping is infact, working, 


	cardViewModel.save =  function(formElelement){
					var jsonData = ko.toJSON(cardViewModel);
					$.ajax({
						url: cardViewModel.resource_uri(),
						type: "PUT",
						data:jsonData,
						//success:function(data) { console.log(data); },
						contentType: "application/json",
						})};

jQuery.easing.def = "easeOutQuart";


// var icons = {header: "ui-icon-circle-arrow-e", headerSelected: "ui-icon-circle-arrow-s"};
// var icons = {secondary: "photoIcon", headerSelected: "ui-icon-circle-arrow-s"};
$("#card_element_toolbar").accordion({
	autoHeight: false,
	collapsible: true,
	// icons: icons,
	active: false,
});

cardViewModel.media_files = ko.observableArray();

//Adding a file from your media files to a card
itemToAdd= new Object();
cardViewModel.add2card = function() {
	itemToAdd.file=this;
	itemToAdd.card= cardViewModel.resource_uri();
	itemToAdd.is_primary= ko.observable(false);
	itemToAdd.is_background=ko.observable(false);
	itemToAdd.title=ko.observable('');
	var jsonData = ko.toJSON(itemToAdd);
	var postURL;
	postURL=$.ajax({
		url: staticel_api_url,
		type: "POST",
		data: jsonData,
		success:function(data) {
			console.log('success and'); 
			console.log(postURL.getResponseHeader('location')); 
			itemToAdd.title=ko.observable('');
			itemToAdd.resource_uri=ko.observable(postURL.getResponseHeader('location'));

			cardViewModel.staticelements.push(itemToAdd);

			},
		// success:function(data) { console.log('success and'); console.log(postURL.getAllResponseHeaders()); },
		contentType: "application/json",
	});
	var itemURL= postURL.getResponseHeader('location');
	// alert(itemURL);
	// itemToAdd.title=ko.observable('');
	// itemToAdd.resource_uri=ko.observable(postURL.getResponseHeader('location'));
	cardViewModel.media_files.remove(this);
	// alert(postURL);
};


cardViewModel.deleteFromCard= function()
{
	console.log("yess lets delete this:");
	$.ajax({
		// url: staticel_api_url + this.id() +'/',
		url: this.resource_uri(),
		type: "DELETE",
		success:function(data) { console.log(data); },
		contentType: "application/json",
	});
	cardViewModel.staticelements.remove(this);

};


//  FLIPINg user editable content so they can edit it. ---------------------------------
// $(".back").hide();
var flip_focal=0;
function mySideChange(front) {
    if (front) {
        $(this).find('.front').show();
        $(this).find('.back').hide();
		$(this).removeClass("ue_active");

        
    } else {
        $(this).find('.front').hide();
        $(this).find('.back').show();
		flip_focal=0;
		$(this).addClass("ue_active");
    }
}

// $(".zue").live('focusin', 
cardViewModel.flipEl=function(event){
		console.log($(event.currentTarget));
		el=event.currentTarget;
		console.log(el);
		$(el).stop().rotate3Di('flip', 500, {
			direction: 'clockwise',
			sideChange: mySideChange,
			complete: function() {if (flip_focal==0) {$(el).find("input:first").focus(); flip_focal=1;}},
			easing: 'easeOutBack' //easeInQuint also good
			}); //end of rotate()

		} 



cardViewModel.unflipEl=function(event){
	el=event.currentTarget;
	$(el).stop().rotate3Di('unflip', 500, {
		sideChange: mySideChange,
		complete: function() 
			{ 	
				console.log('DONE');
				console.log(this);
				// ko.mapping.updateFromJS(cardViewModel, this); 
				var jsonData = ko.toJSON(this);
				//save the changes on the elemnt to the server
				$.ajax({
					url: this.resource_uri(),
					type: "PUT",
					data:jsonData,
					success:function(data) { console.log(data); },
					contentType: "application/json",
					});				
			}.bind(this)//end complete (of spin) function
	});//end 3d spin
	// console.log(this);

	console.log('bye');
}

// alert('The length of the array is ' + cardViewModel.staticelements().length);


cardViewModel.marked_text = ko.dependentObservable(function() {
	if (this.text() =='')
		return ''
	return converter.makeHtml(this.text());
},cardViewModel);

cardViewModel.mediaPostProcessingLogic= function(elements){
	// console.log(elements);
	$(elements).find("a.uibutton").button();
}


//**********************************************
//******      SIDEBAR CODE              ********
//**********************************************

cardViewModel.media_type= ko.observable("Media");
cardViewModel.input_type= ko.observable("Input");

cardViewModel.changeMediaType= function(event){
	cardViewModel.media_type($(event.currentTarget).data("media_type"));
}

cardViewModel.changeInputType= function(event){
	cardViewModel.input_type($(event.currentTarget).data("input_type"));
}
cardViewModel.changeInputTypeBack= function(event){
	cardViewModel.input_type("Input")
}

cardViewModel.changeMediaTypeBack= function(event){
	cardViewModel.media_type("Media")
}


// pick image, video, audio or other.
$("#add_media_group h4, #add_media img").click(function(event){
	// stop it from opening and closing the acordian
	event.stopPropagation(); 	
	cardViewModel.media_type($(this).data("media_type"));
	
	$.getJSON(file_api_url + "?type="+cardViewModel.media_type(), function(data) {
		$("#add_media_group h4").slideUp();
		for (x in  data.objects){cardViewModel.media_files.push(data.objects[x]);}
		});	
	// ko.applyBindings(cardViewModel);
	
	// alert(cardViewModel.media_type());
});



ko.applyBindings(cardViewModel);


// $(".uibutton").button();

});// end docready




