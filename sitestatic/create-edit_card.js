var card_api_url='/api/v1/card/';
var staticel_api_url='/api/v1/mediaelement/';
var input_api_url='/api/v1/inputelement/';
var action_api_url='/api/v1/action/';
var file_api_url='/api/v1/userfile/';
var guide_api_url='/api/v1/guide/';
// var smallcard_api_url='/api/v1/smallcard/';

var VM; //our viewmodel
var converter = new Showdown.converter();

var initial_card_object;
var mapping;

// DOOOOCCCCCCCCCCCCCCCRRRRRRRRREEEEEEEEEADDDDDDDDDDDDDDDDDDDYYYYYYYYYYYYYYYY
$(document).ready(function(){	
$(".uibutton").button();

jQuery.easing.def = "easeOutQuart";

//initial mapping
// mapping = {
//     'mediaelements': {
//         key: function(data) {
// 			// console.log(data.resource_uri);
//             return ko.utils.unwrapObservable(data.resource_uri);
//         					}
// 						}
// 			}

initial_card_object= jQuery.parseJSON(initial_card_json);
VM = ko.mapping.fromJS(initial_card_object, mapping);
//// or
// VM = ko.mapping.fromJSON(initial_card_json, mapping); 	// console.log(initial_card_object);
// VM.mediaelements.mappedRemove({ resource_uri : '/api/v1/staticelement/4/' });
//this line works, so the mapping is infact, working, 



//************************
//****   SAVE THE CARD ***  - NO LONGER NECCESARY, THE UNFLIPING FUNCTION ENDED UP GENERALIZED! 
//								huzzah i am smart?
//************************
VM.save = function(formElelement)
{
	var jsonData = ko.mapping.toJSON(VM);
	// alert('hi');
	$.ajax({
		url: VM.resource_uri(),
		type: "PUT",
		data:jsonData,
		//success:function(data) { console.log(data); },
		contentType: "application/json",
		})
};





// ****************************************************
//       ADDING MEDIA FILE TO CARD AS MEDIA ELEMENT   *
// ****************************************************
itemToAdd= new Object();
VM.media_files = ko.observableArray(); //this needs to be here as we're referencing it in addMedia2card
VM.addMedia2card = function() {
	// console.log(this);
	this.file= ko.observable(this.file);
	itemToAdd.file=this; //this was equal simply to this, which works for adding'em, making it observable
	itemToAdd.type = ko.observable(this.type);
	itemToAdd.card= VM.resource_uri();
	
	itemToAdd.is_background=ko.observable(false);
	itemToAdd.title=ko.observable('');
	var jsonData = ko.toJSON(itemToAdd);
	var postURL;
	postURL=$.ajax({
		url: staticel_api_url,
		type: "POST",
		data: jsonData,
		success:function(data) {
			// console.log('success and'); 
			// console.log(postURL.getResponseHeader('location')); 
			itemToAdd.title=ko.observable();
			itemToAdd.resource_uri=ko.observable(postURL.getResponseHeader('location'));
			itemToAdd.id = itemToAdd.resource_uri().match(/\/mediaelement\/(.*)\//)[1];
			uri_string_n=itemToAdd.resource_uri().indexOf('api');
			rid= itemToAdd.resource_uri().slice(uri_string_n-1);
			if (VM.mediaelements().length==0)
				VM.primary_media(rid);
			//add the element to the card
			VM.mediaelements.push(itemToAdd);
			},
		contentType: "application/json",
	});
	//remove it from the media files. up for discussion
	
	VM.media_files.remove(this);

};


VM.deleteFromCard= function()
{
	console.log("yess lets delete this:");
	$.ajax({
		url: this.resource_uri(),
		type: "DELETE",
		success:function(data) { console.log(data); },
		contentType: "application/json",
	});
	// alert(VM.mediaelements.indexOf(this));
	
	//what kind of element are we deleting?
	if (VM.mediaelements.indexOf(this)!=-1)
		VM.mediaelements.remove(this);
		
	if (VM.inputelements.indexOf(this)!=-1)
		VM.inputelements.remove(this);
};


//********************************************
//****   FLIPING USER EDITABLE ELEMENTS    ***
//********************************************

$(".back").hide();
var flip_focal=0;
function mySideChange(front) {
    if (front) {
        $(this).find('.front').show();
        $(this).find('.back').hide();
		$(this).removeClass("ue_active");
	}
 	else {
        $(this).find('.front').hide();
        $(this).find('.back').show();
		flip_focal=0;
		$(this).addClass("ue_active");
    }
}
 
VM.flipEl=function(event){
		el=event.currentTarget;
		$(el).stop().rotate3Di('flip', 500, {
			direction: 'clockwise',
			sideChange: mySideChange,
			complete: function() {if (flip_focal==0) {$(el).find("textarea:first").focus(); $(el).find("input:first").focus(); flip_focal=1;}},
			easing: 'easeOutBack' //easeInQuint also good
			}); //end of rotate()
		} 

VM.unflipEl=function(event){
	el=event.currentTarget;
	$(el).stop().rotate3Di('unflip', 500, {
		sideChange: mySideChange,
		complete: function() 
			{ 	
				var jsonData = ko.mapping.toJSON(this);
				//save the changes on the elemnt to the server // TODO check if the data changed, duh! TODO also maybe keep it from sending the elements, that's wasteful 
				console.log(jsonData);
				$.ajax({
					url: this.resource_uri(),
					type: "PUT",
					data:jsonData,
					success:function(data) { console.log(data); },
					contentType: "application/json",
					});				
			}.bind(this)//end complete (of spin) function
	});//end 3d spin


	console.log('bye');
}

//apply button() to media elements after they've been added
VM.uePostProcessing= function(element){
	// console.log(element);
	// if ($(element).hasClass('uibutton'))
		// element.button();
	$(element).find(".uibutton").button();
}

//**********************************************
//******      DEFINE DIFFERENT MEDIA TEMPLATES, PRIMARY, BG OR NOT  ********
//**********************************************
VM.mediaTypeTemplate= function(element){
	if (element.type()=="image")
		return 'imageTemplate';
	if (element.type()=="video")
		return 'videoTemplate';
}

VM.primarymediaTypeTemplate= function(element){
	if (element.resource_uri() == VM.primary_media())
		return 'primaryImageTemplate';
		
	else 
		return 'nodisplay';
}

//for the sidebar, add media
VM.userFileDisplayMode= function(element){
	console.log(element);
	if (element.type=="image")
		return 'userFileImageTemplate';
	if (element.type=="video")
		return 'userFileVideoTemplate';
	if (element.type=="audio")
		return 'userFileAudioTemplate';	
	else (element.type=="other")
		return 'userFileOtherTemplate';	



	// if (VM.currently_adding_media_type()=="image")
	// 	return 'userFileImageTemplate';
	// if (VM.currently_adding_media_type()=="video")
	// 	return 'userFileVideoTemplate';
	// if (VM.currently_adding_media_type()=="audio")
	// 	return 'userFileAudioTemplate';	
	// if (VM.currently_adding_media_type()=="other")
	// 	return 'userFileOtherTemplate';	
	// if (VM.currently_adding_media_type()=="upload")
	// 	return 'userFileUploadTemplate';

}

VM.inputTypeTemplate= function(element){
// this will return differently based on if it's image, video, audio (or bg?)
		return 'buttonTemplate';
}


//**********************************************
//******      APPLY MARKDOWN  MARKUP    ********
//**********************************************
VM.marked_text = ko.dependentObservable(function() {
	if (!this.text())
		return null;
	return converter.makeHtml(this.text());
},VM);


//**********************************************
//******      SIDEBAR CODE              ********
//**********************************************

$("#card_element_toolbar").accordion({
	autoHeight: false,
	collapsible: true,
	// icons: icons,
	active: false,
});

VM.media_type= ko.observable("Media");
VM.input_type= ko.observable("Input");
VM.currently_adding_input_type= ko.observable();
VM.currently_adding_media_type= ko.observable();

VM.changeMediaType= function(event){
	VM.media_type($(event.currentTarget).data("media_type"));
}

VM.changeInputType= function(event){
	VM.input_type($(event.currentTarget).data("input_type"));
}

VM.changeInputTypeBack= function(event){
	if (!VM.currently_adding_input_type())
		VM.input_type("Input");
	else
		VM.input_type(VM.currently_adding_input_type());
}

VM.changeMediaTypeBack= function(event){
	if (!VM.currently_adding_media_type())
		VM.media_type("Media")
	else
		VM.media_type(VM.currently_adding_media_type());
}


// ******************************************
// **  LOAD MEDIA/USERFILES TO PICK FROM  ***
// ******************************************
$("#add_media_group h4, #add_media img").click(function(event){
	// stop it from opening and closing the acordian
	var current_accordian_index = $("#card_element_toolbar").accordion( "option", "active" )
	// console.log(current_accordian_index);

	 if (current_accordian_index===0) //so it's already open to the first element, media
			event.stopPropagation(); 	
	
	VM.media_type($(this).data("media_type"));
	VM.currently_adding_media_type($(this).data("media_type"));

	if (VM.media_type()=='upload')
		{
			showFileUploadForm();
			return true;
		}
	
	if (VM.media_type()=='media')
	{
		$.getJSON(file_api_url, function(data) {
		VM.media_files.removeAll();
		for (x in data.objects)
			{VM.media_files.push(data.objects[x]);}
		});	 ///end json
		console.log('alllll media files?')
		return;
	}

	
	
	$.getJSON(file_api_url + "?type="+VM.media_type(), function(data) {
		VM.media_files.removeAll();
		for (x in data.objects)
			{VM.media_files.push(data.objects[x]);}
		});	 ///end json
	
}); //end click


$("#add_input_group h4, #add_input img").click(function(event){
	// stop it from opening and closing the acordian
	var current_accordian_index = $("#card_element_toolbar").accordion( "option", "active" )
	VM.currently_adding_input_type($(this).data("input_type"));

	// console.log(current_accordian_index);

	 if (current_accordian_index===1) //so it's open to the second element
		{
			event.stopPropagation(); 	
		}

		// $("#add_input_group h4").slideUp();


}); //end click


VM.newCardTitle= ko.observable();
VM.newButtonText= ko.observable();
VM.newActionGotoCard = ko.observable();



//REPLACE CARDS WITH GUIDE TODO because guide has the relevant info about each card anyway
VM.all_cards = ko.observableArray();
var json_all_cards = jQuery.parseJSON(all_cards);
for (x in json_all_cards)
	{
		VM.all_cards.push(json_all_cards[x]);
	}


VM.addInput2card= function(){


	if (VM.newActionGotoCard()=='addcard')
		{	
			console.log('addcarding');
			cardToAdd= new Object();
			cardToAdd.title= VM.newCardTitle();			
			cardToAdd.guide= VM.guide();			
			var postURL_newcard;
			jsonData = ko.toJSON(cardToAdd);
			
			postURL_newcard=$.ajax({
				url: card_api_url,
				type: "POST",
				data: jsonData,
				success:function(data) {
					console.log('--');
					// console.log(postURL_newcard.getResponseHeader('content-location'));
					new_card_uri= postURL_newcard.getResponseHeader('location');
					uri_string_n=new_card_uri.indexOf('api');
					new_card_uri= new_card_uri.slice(uri_string_n-1)
					console.log(new_card_uri);
					cardToAdd.resource_uri=ko.observable(new_card_uri);
					cardToAdd.id = cardToAdd.resource_uri().match(/\/card\/(.*)\//)[1];
					VM.all_cards.push(cardToAdd);
					VM.newActionGotoCard(cardToAdd.resource_uri());
					addInputHelper();
				},
			contentType: "application/json",	
		});
		
	} //end if
	
	else
	{
		addInputHelper();
	}
	
}// end addInput2card function




ko.applyBindings(VM);

$(".uibutton").button();


});// end docready


// HEEEEEEEEEEEEEEEEELLLLLLLLLLLLLLLLLLLLLLLLLLPPPPPPPPPPPPPPPPPPPEEEEEERRRRRRRRRRRRRRRRRRRs

addInputHelper =function(){
	
	inputToAdd= new Object();
	newAction = new Object();
	newAction.goto =ko.observable(VM.newActionGotoCard());
	newAction.id = null;
	var postURL_input;
	inputToAdd.card= VM.resource_uri();
	inputToAdd.button_text= ko.observable( VM.newButtonText());
	inputToAdd.default_action= newAction;  //maybe this should be observable?
	jsonData = ko.toJSON(inputToAdd);

	postURL_input=$.ajax({
		url: input_api_url,
		type: "POST",
		data: jsonData,
		success:function(data) {
			// console.log(data); 
			inputToAdd.resource_uri=ko.observable(postURL_input.getResponseHeader('location'));
			// console.log(postURL_input.getResponseHeader('location'));
			inputToAdd.id = inputToAdd.resource_uri().match(/\/inputelement\/(.*)\//)[1];
			// match(/\/inputelement\/(.*)\//)[1]
			VM.inputelements.push(inputToAdd); //WHAT? TODO
			},
		contentType: "application/json",
		});
	} //end input adding function


