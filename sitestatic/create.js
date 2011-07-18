var card_api_url='/api/v1/card/';
var staticel_api_url='/api/v1/mediaelement/';
var input_api_url='/api/v1/inputelement/';
var action_api_url='/api/v1/action/';
var file_api_url='/api/v1/userfile/';

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
	alert('hi');
	$.ajax({
		url: VM.resource_uri(),
		type: "PUT",
		data:jsonData,
		//success:function(data) { console.log(data); },
		contentType: "application/json",
		})
};

// ****************************************
//Adding a file from user's media files to the card
// ****************************************
itemToAdd= new Object();
VM.media_files = ko.observableArray(); //this needs to be here as we're referencing it in addMedia2card
VM.addMedia2card = function() {
	// console.log(this);
	this.file= ko.observable(this.file);
	itemToAdd.file=this; //this was equal simply to this, which works for adding'em, making it observable
	itemToAdd.card= VM.resource_uri();
	if (VM.mediaelements().length==0)
		itemToAdd.is_primary= ko.observable(true); //should primary default to true or false? 
	else
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
				//save the changes on the elemnt to the server 
				// TODO check if the data changed, duh!
				// alert('hi');
				// TODO also maybe keep it from sending the elements, that's wasteful 
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
VM.uePostProcessing= function(elements){
	// console.log(elements);
	$(elements).find(".uibutton").button();
}

//**********************************************
//******      DEFINE DIFFERENT MEDIA TEMPLATES, PRIMARY, BG OR NOT   (not currently implimented) ********
//**********************************************
VM.mediaTypeTemplate= function(element){
// this will return differently based on if it's image, video, audio (or bg?)
		return 'imageTemplate';
}

VM.inputTypeTemplate= function(element){
// this will return differently based on if it's image, video, audio (or bg?)
		return 'buttonTemplate';
}


//**********************************************
//******      APPLY MARKDOWN  MARKUP    ********
//**********************************************
VM.marked_text = ko.dependentObservable(function() {
	if (this.text() =='')
		return ''
	return converter.makeHtml(this.text());
},VM);

//**********************************************
//******      SIDEBAR CODE              ********
//**********************************************

// var icons = {header: "ui-icon-circle-arrow-e", headerSelected: "ui-icon-circle-arrow-s"};
// var icons = {secondary: "photoIcon", headerSelected: "ui-icon-circle-arrow-s"};
$("#card_element_toolbar").accordion({
	autoHeight: false,
	collapsible: true,
	// icons: icons,
	active: false,
});

VM.media_type= ko.observable("Media");
VM.input_type= ko.observable("Input");

VM.changeMediaType= function(event){
	VM.media_type($(event.currentTarget).data("media_type"));
}

VM.changeInputType= function(event){
	VM.input_type($(event.currentTarget).data("input_type"));
}
VM.changeInputTypeBack= function(event){
	// TODO don't change it back if the accordian is open to this. or rather, change it 
	VM.input_type("Input")
}

VM.changeMediaTypeBack= function(event){
	VM.media_type("Media")
}




// ******************************************
// **  LOAD MEDIA/USERFILES TO PICK FROM  ***
// ******************************************
$("#add_media_group h4, #add_media img").click(function(event){
	// stop it from opening and closing the acordian
	event.stopPropagation(); 	
	VM.media_type($(this).data("media_type"));
	
	$.getJSON(file_api_url + "?type="+VM.media_type(), function(data) {
		$("#add_media_group h4").slideUp();
		for (x in  data.objects)
			{
				VM.media_files.push(data.objects[x]);
			}
		});	 ///end json
	// ko.applyBindings(VM);
}); //end click

// *************************************
// ****     CREATE INPUT ELEMENTS    ***
// *************************************
$("#add_input_group h4, #add_input img").click(function(event){
	// stop it from opening and closing the acordian
	event.stopPropagation();
	// VM.input_type($(this).data("input_type"));
}); //end click

VM.newCardTitle= ko.observable('');
VM.newButtonText= ko.observable('');
VM.newActionGotoCard = ko.observable('');

inputToAdd= new Object();
VM.addInput2card= function(){
	
	// console.log(newAction);
	// var jsonData = ko.toJSON(newAction);
	newAction = new Object();
	newAction.goto =ko.observable(VM.newActionGotoCard());
	newAction.id = null;
	
	var postURL_input;
	inputToAdd.card= VM.resource_uri();
	inputToAdd.button_text= ko.observable( VM.newButtonText());
	inputToAdd.default_action= newAction;
	jsonData = ko.toJSON(inputToAdd);

	postURL_input=$.ajax({
		url: input_api_url,
		type: "POST",
		data: jsonData,
		success:function(data) {
			console.log('success: '); 
			console.log(data); 
			
			// so data.default_action is the uri  TODO
			
			// console.log(postURL_input.getResponseHeader('location')); 
			inputToAdd.resource_uri=ko.observable(postURL_input.getResponseHeader('location'));
			//add the element to the card
			// inputToAdd.default_action=newAction;
			VM.inputelements.push(inputToAdd); //WHAT? TODO
			},
		contentType: "application/json",
		});
	}

	
// } // end adding input function



ko.applyBindings(VM);

$(".uibutton").button();



});// end docready




