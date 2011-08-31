var card_api_url='/api/v1/card/';
var staticel_api_url='/api/v1/mediaelement/';
var input_api_url='/api/v1/inputelement/';
var map_api_url='/api/v1/mapelement/';
var mappoint_api_url='/api/v1/mappointelement/';
var action_api_url='/api/v1/action/';
var file_api_url='/api/v1/userfile/';
var guide_api_url='/api/v1/guide/';
var timer_api_url='/api/v1/timer/';
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

VM.the_primary_media_object = ko.observableArray();
if (primary_media_json)
	VM.the_primary_media_object.push(ko.mapping.fromJS(jQuery.parseJSON(primary_media_json)));


//************************
//****   SAVE THE CARD ***  - NO LONGER NECCESARY, THE UNFLIPING FUNCTION ENDED UP GENERALIZED! 
//								huzzah i am smart?
//************************
VM.save = function()
{
	var jsonData = ko.mapping.toJSON(VM);
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

VM.media_files = ko.observableArray(); //this needs to be here as we're referencing it in addMedia2card
VM.addMedia2card = function() {
	itemToAdd= new Object();
	// console.log(this);
	this.file= ko.observable(this.file);
	itemToAdd.file=this; //this was equal simply to this, which works for adding'em, making it observable
	itemToAdd.type = ko.observable(this.type);
	itemToAdd.card= VM.resource_uri();
	// itemToAdd.is_background=ko.observable(false);
	itemToAdd.title=ko.observable('');
	var jsonData = ko.toJSON(itemToAdd);
	var postURL;
	
	postURL=$.ajax({
		url: staticel_api_url,
		type: "POST",
		data: jsonData,
		success:function(data) {

			itemToAdd.title=ko.observable();
			itemToAdd.autoplay=ko.observable();
			itemToAdd.id = postURL.getResponseHeader('location').match(/\/mediaelement\/(.*)\//)[1];
			itemToAdd.resource_uri=ko.observable(staticel_api_url + itemToAdd.id +'/');
			console.log('itemToAdd:');
			console.log(itemToAdd);
			//make primary if there is no other media
			if (VM.mediaelements().length < 1)
				{	VM.the_primary_media_object.push(itemToAdd);
					VM.primary_media(staticel_api_url + itemToAdd.id + '/' );
					console.log('made primary');
					console.log(VM.primary_media());
					VM.save();
				}
			
			//add the element to the card
			VM.mediaelements.push(itemToAdd);
			
			},
		contentType: "application/json",
	});
	//remove it from the media files. up for discussion
	
	VM.media_files.remove(this);

};

// TODO BUG when loading from an existing card, deleting the primary media doesn't delete the thumb of it.
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
	
	if (VM.mediaelements.indexOf(this)!=-1)
		VM.mediaelements.remove(this);
	

	if (VM.the_primary_media_object().length)
	{
		if (VM.the_primary_media_object()[0].resource_uri()==this.resource_uri())
			{
				VM.the_primary_media_object.pop();
				VM.primary_media(null);
				for (el in VM.mediaelements())
					{
						console.log(el);
						if (VM.mediaelements()[el].resource_uri()==this.resource_uri())
							VM.mediaelements.splice(el, 1);
					}
			}
	}
	
	if (VM.inputelements.indexOf(this)!=-1)
		VM.inputelements.remove(this);
		
	if (VM.mapelements.indexOf(this)!=-1)
		VM.mapelements.remove(this);
};


VM.makePrimary = function()
{
	console.log("lets make it primary");
	d=VM.the_primary_media_object.pop();
	console.log(d);
	VM.the_primary_media_object.push(this);
	VM.primary_media(this.resource_uri());
	VM.save();
}


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
		
			emphasizeContent();
		
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


	console.log('saved' + el);
}

//apply button() to media elements after they've been added
VM.uePostProcessing= function(element){
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
	if (element.type()=="audio")
		return 'audioTemplate';
	if (element.type()=="other")
		return 'otherTemplate';		
}

// VM.primarymediaTypeTemplate= function(element){
// 	if (element.resource_uri() == VM.primary_media())
// 		return 'primaryImageTemplate';
// 		
// 	else 
// 		return 'nodisplay';
// }

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



}

VM.inputTypeTemplate= function(element){
	console.log(element);
	
		if (element.type()=="button")
			return 'buttonTemplate';
		if (element.type() == 'timer')
			return 'timerTemplate';
		if (element.type() == 'map')
			return 'mapTemplate';
		else			
			return 'errorNoTemplate';
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
}).bind("accordionchangestart", function(event, ui){
	console.log('accordian startchange!');

	if (ui.newHeader.length)
		emphasizeSidebar();
	else
		emphasizeContent();
}); //end bind to accordian changestart



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

	emphasizeSidebar();

	 if (current_accordian_index===0) //so it's already open to the first element, media
			event.stopPropagation(); 	
	
	VM.media_type($(this).data("media_type"));
	VM.currently_adding_media_type($(this).data("media_type"));

	if (VM.media_type()=='upload')
		{
			VM.media_files.removeAll();

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
	
	emphasizeSidebar();

	// console.log(current_accordian_index);

	 if (current_accordian_index===1) //so it's open to the second element
		{
			event.stopPropagation(); 	
		}

		// $("#add_input_group h4").slideUp();


}); //end click


VM.newCardTitle= ko.observable();
VM.newButtonText= ko.observable();
VM.newMapText= ko.observable();
VM.newActionGotoCard = ko.observable();
VM.newTimerSeconds = ko.observable(00)
VM.newTimerMinutes = ko.observable(00)


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
			console.log(jsonData);
			postURL_newcard=$.ajax({
				url: card_api_url,
				type: "POST",
				data: jsonData,
				success:function(data) {
					console.log('success creating a new card');
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


VM.addMap2Card= function(){
	mapToAdd= new Object();
	var postURL_input;
	mapToAdd.type= ko.observable('map');
	mapToAdd.card= VM.resource_uri();
	mapToAdd.map_title= ko.observable( VM.newMapText());
	jsonData = ko.toJSON(mapToAdd);
	postURL_input=$.ajax({
		url: map_api_url,
		type: "POST",
		data: jsonData,
		success:function(data) {
				console.log('map added!');	
				console.log(data); 
				mapToAdd.resource_uri=ko.observable(postURL_input.getResponseHeader('location'));
				mapToAdd.id = mapToAdd.resource_uri().match(/\/mapelement\/(.*)\//)[1];
				VM.mapelements.push(mapToAdd); 
			},
		contentType: "application/json",
		});
} 
	
	
VM.addPoint2Map= function(point){
	pointToAdd= new Object();
	var postURL_input;
	pointToAdd.point= point;
	//pointToAdd.point_title = VM.resource_uri();
	//pointToAdd.manual_addy = ko.observable( VM.newMapText());
	jsonData = ko.toJSON(pointToAdd);
	console.log(jsonData);
	postURL_input=$.ajax({
		url: mappoint_api_url,
		type: "POST",
		data: jsonData,
		success:function(data) {
				console.log('point added!');	
				console.log(data); 
				pointToAdd.resource_uri=ko.observable(postURL_input.getResponseHeader('location'));
				pointToAdd.id = pointToAdd.resource_uri().match(/\/mappointelement\/(.*)\//)[1];
				//VM.mappointelements.push(pointToAdd); 
			},
		contentType: "application/json",
		});
} 

// **************************************
// ******      File Upload Plugin    ****
// **************************************

$('#fileupload').fileupload({
// options
	autoUpload: true,
}).bind('fileuploaddragover', 
	function (e){ 
			console.log('drop it!');
			$("#add_media_group").css({backgroundColor: "#feb912"});

		}).bind('fileuploaddrop', 
	function(e, data){
			console.log('dropped it!');				
			$("#add_media_group").css({backgroundColor: "#ffffff"});

	}).bind('fileuploaddone',
	function (e, data) {
		
		$("#add_media_group").css({backgroundColor: "#ffffff"});

		$("table.files").hide();
		$("#fileupload, .fileupload-content").slideUp();
		
		//this shouldn't be hardcoded, it should be all, and the templates should be per userfile, not by the VM.media_Type
		VM.currently_adding_media_type('media');
		VM.media_type('media');

		console.log('done uploading!');				
		$.getJSON(file_api_url, function(data) {
			VM.media_files.removeAll();
			for (x in data.objects)
				{VM.media_files.push(data.objects[x]);}
		});	 ///end json
		return
}); //end blind



$('#fileupload .files a:not([target^=_blank])').live('click', function (e) {
    e.preventDefault();
    $('<iframe style="display:none;"></iframe>')
        .prop('src', this.href)
        .appendTo('body');
});





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
	inputToAdd.type= ko.observable(VM.currently_adding_input_type());
	if (inputToAdd.type() == 'timer')
		{
			inputToAdd.seconds= VM.newTimerSeconds();
			inputToAdd.minutes= VM.newTimerMinutes();
		}
	inputToAdd.button_text= ko.observable( VM.newButtonText());
	inputToAdd.default_action= newAction;  //maybe this should be observable?
	jsonData = ko.toJSON(inputToAdd);
	console.log(jsonData);
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
			VM.inputelements.push(inputToAdd); 
			},
		contentType: "application/json",
		});
		
		VM.newCardTitle('');
		VM.newButtonText('');
		VM.newActionGotoCard('');
		VM.newTimerMinutes(0);
		VM.newTimerSeconds(0);
		$("#card_element_toolbar").accordion("activate", false);
		VM.input_type("Input");
		VM.currently_adding_input_type('');
	
	} //end input adding function

emphasizeContent = function()
{
	// $("#content").removeClass("smaller").addClass("bigger");
	// $("#sidebar").removeClass("bigger").addClass("smaller");
}

emphasizeSidebar= function()
{
	// $("#content").removeClass("bigger").addClass("smaller");
	// $("#sidebar").removeClass("smaller").addClass("bigger");
}



