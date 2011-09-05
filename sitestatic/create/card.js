var card_api_url='/api/v1/card/';
var media_api_url='/api/v1/mediaelement/';
var input_api_url='/api/v1/inputelement/';
var map_api_url='/api/v1/mapelement/';
var action_api_url='/api/v1/action/';
var file_api_url='/api/v1/userfile/';
var guide_api_url='/api/v1/guide/';
var timer_api_url='/api/v1/timer/';
// var smallcard_api_url='/api/v1/smallcard/';

var VM; //our viewmodel
var converter = new Showdown.converter();

var initial_card_object;
var mapping;

// ***********************************************
// ***********       DOCREAD         *************
// ***********************************************
$(document).ready(function(){	

// Make stuff pretty
	jQuery.easing.def = "easeOutQuart";


//Prep inital data for card that's been saved previously and has existing

	initial_card_object= jQuery.parseJSON(initial_card_json);
	VM = ko.mapping.fromJS(initial_card_object);
	
	$.each(VM.mediaelements(), function (index, element) {
		element.client_id = ko.observable('media'+ element.id());
		element.existing = ko.observable(true);

		if (element.external_file())
		{
			element.file_url = ko.observable(element.external_file());
			element.medium_url = ko.observable(element.external_file());
		}
		else
		{
			element.file_url = ko.observable(element.file.display_url());
			element.medium_url = ko.observable(element.file.medium_url());
		}

	});
	
	VM.primary_media =ko.dependentObservable(function() {
	    return VM.mediaelements()[0]
	}, VM);

	VM.check_if_primary = function(element)
	{
		console.log("element");
		console.log(element);
		if (element == VM.primary_media())
			return true;
		else
			return false;
	}

	VM.makePrimary = function()
	{
		console.log("lets make this primary");
		console.log(this);
		VM.mediaelements.remove(this);
		VM.mediaelements.unshift(this);
		// d=VM.the_primary_media_object.pop();
		// console.log(d);
		// VM.the_primary_media_object.push(this);
		// VM.primary_media(this.resource_uri());
		// VM.save_element();
	}
	
	// 
	// VM.the_primary_media_object = ko.observableArray();
	// if (primary_media_json)
	// 	VM.the_primary_media_object.push(ko.mapping.fromJS(jQuery.parseJSON(primary_media_json)));
		

// **************************************
// ******      File Upload Plugin    ****
// **************************************

	$('#fileupload').fileupload({
	// options
		autoUpload: true,
		previewMaxWidth: 500,
		previewMaxHeight: 500
	}).bind('fileuploaddragover', 
		function (e){ 
				console.log('drop it!');
				$(this).css({backgroundColor: "#feb912"});

	}).bind('fileuploadadd', 
		function(e, data){
				$(".adder.media").fadeOut('fast', function(){$(this).addClass('minimized').delay(100).fadeIn();});
				console.log('dropped it (Added it, really)!');
				media_holder=$("#media");
				
				//Pre Upload, File is added, preview is created if it's an image
				$.each(data.files, function (index, file) {
						        // console.log('Added file: ' + file.name);
								// console.log(file)
								var new_media_element = new Object();
								new_media_element.title = ko.observable(); //ko.observable(file.name.split('.')[0]);
								new_media_element.file_url = ko.observable();
								new_media_element.type = ko.observable(file.type.split('/')[0]);
								new_media_element.client_id = ko.observable('media' + file.name.split('.')[0].split(' ')[0] + file.size);
								new_media_element.card= VM.resource_uri();
								new_media_element.resource_uri= ko.observable();
								new_media_element.external_file= ko.observable();
								new_media_element.medium_url= ko.observable();
																
								var id_string = "#" + new_media_element.client_id();
								$(id_string).addClass("uploading")
								// the_element_jq= $("#" + new_media_element.client_id()).addClass("uploading");

								if (new_media_element.type() =='image')
								{
									$('#fileupload').data('fileupload')._loadImage(file, function (img) {
					                    // console.log(img.src);
										new_media_element.medium_url(img.src);
										// $(id_string).find('.preview_image').attr("src", img.src).fadeIn();
										// $(img).clone().hide().prependTo($(id_string).find('.preview_wrapper')).fadeIn().attr("class", "preview_image");
										}, //end callback
										$('#fileupload').fileupload('option') ); //end _loadimage
								}
								else
								{
									img = $("<img src='/static/img/upload-icon.png'/>")
								    $(img).hide().prependTo($(id_string).find('.preview_wrapper')).fadeIn().attr("class", "preview_image");	
								}
								
								VM.mediaelements.push(new_media_element);
								
								
						}); //end each	

				// console.log(data);

				$("#add_media_group").css({backgroundColor: "#ffffff"});


	}).bind('fileuploaddone',
		function (e, data) {

			$(this).css({backgroundColor: "#ffffff"});
			console.log('done uploading!');
			
			//File has been uploaded, now lets associated it with what's actually on the server.
			$.each(data.files, function (index, file) {
				var client_id = 'media' + file.name.split('.')[0].split(' ')[0] + file.size;
				var id_string = "#" + client_id;
				// var the_element_jq= $("#" + client_id);
				
				var the_element_ko = ko.utils.arrayFirst(VM.mediaelements(), function(item) { return item.client_id() === client_id;})

				// console.log(the_element_jq);
				// console.log(the_element_ko.client_id());

				the_element_ko.file_url(data.result[0].url);
				the_element_ko.resource_uri(media_api_url + data.result[0].id + '/');
				the_element_ko.medium_url(data.result[0].medium_image_url);
				// $(id_string).find('.preview_image').attr('src', data.result[0].medium_image_url).attr('id', client_id + 'img'); // messing up because if data.result.mediumimageurl is empty, acts as a getter
				$(id_string).removeClass('uploading');
				// console.log('data.result[url]'); 
				// console.log(data.result);
				
			}); //end each data.files
			
			return
	}); //end binds

	$('#fileupload .files a:not([target^=_blank])').live('click', function (e) {
	    e.preventDefault();
	    $('<iframe style="display:none;"></iframe>')
	        .prop('src', this.href)
	        .appendTo('body');
	});
	
	// END UPLOAD PLUGIN


	// Save Element
	VM.save_element = function()
	{
		var that = this;
		delete that.file_url;
		delete that.client_id;
		delete that.existing;
		delete that.medium_url;
		delete that.file;
		delete that.doesnotexistthing;
		
		var jsonData = ko.mapping.toJSON(that);
		$.ajax({
			url: that.resource_uri(),
			type: "PUT",
			data:jsonData,
			success:function(data) { 
				console.log(data); 
				},
			contentType: "application/json",
			});
	}

	//Save Card
	
	VM.save_card = function()
	{
		//this was for use with the api if readonly=false, to save the whole dang card at once foreal
		// var mappedItems = ko.utils.arrayMap(VM.mediaelements(), function(item) {
		//     delete item.file_url;
		//     delete item.client_id;
		//     delete item.existing;
		//     delete item.medium_url;
		//     item.file = item.file.resource_uri();
		//     return item;
		// })
		// VM.mediaelements(mappedItems);
		
		var jsonData = ko.mapping.toJSON(VM);
		$.ajax({
			url: VM.resource_uri(),
			type: "PUT",
			data:jsonData,
			//success:function(data) { console.log(data); },
			contentType: "application/json",
			})
	};

	// Aviary Launcher!  
	VM.editImage = function()
	{	
	featherEditor.launch({ 
		image: this.client_id() + 'img', //the id of the actual image ends in img
		url: this.file_url()
			});
	}//

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


		if (VM.inputelements.indexOf(this)!=-1)
			VM.inputelements.remove(this);

		if (VM.mapelements.indexOf(this)!=-1)
			VM.mapelements.remove(this);
	};
	
	
	//**********************************************
	//******      APPLY MARKDOWN  MARKUP    ********
	//**********************************************
	VM.marked_text = ko.dependentObservable(function() {
		if (!this.text())
			return null;
		return converter.makeHtml(this.text());
	},VM);
	
	
	
	
	


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
			url: media_api_url,
			type: "POST",
			data: jsonData,
			success:function(data) {

				itemToAdd.title=ko.observable();
				// itemToAdd.autoplay=ko.observable();
				itemToAdd.id = postURL.getResponseHeader('location').match(/\/mediaelement\/(.*)\//)[1];
				itemToAdd.resource_uri=ko.observable(media_api_url + itemToAdd.id +'/');
				console.log('itemToAdd:');
				console.log(itemToAdd);
				//make primary if there is no other media
				if (VM.mediaelements().length < 1)
					{	VM.the_primary_media_object.push(itemToAdd);
						VM.primary_media(media_api_url + itemToAdd.id + '/' );
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



	// 
	// VM.makePrimary = function()
	// {
	// 	console.log("lets make it primary");
	// 	d=VM.the_primary_media_object.pop();
	// 	console.log(d);
	// 	VM.the_primary_media_object.push(this);
	// 	VM.primary_media(this.resource_uri());
	// 	VM.save();
	// }




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
		// console.log(element);
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
	//******      SIDEBAR CODE              ********
	//**********************************************


	$("#card_element_toolbar").accordion({
		autoHeight: false,
		collapsible: true,
		// icons: icons,
		active: false,
	}).bind("accordionchangestart", function(event, ui){
		console.log('accordian startchange!');


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
		inputToAdd= new Object();
		var postURL_input;
		inputToAdd.type= ko.observable('map');
		inputToAdd.card= VM.resource_uri();
		inputToAdd.title=ko.observable("Map");
		jsonData = ko.toJSON(inputToAdd);
		postURL_input=$.ajax({
			url: map_api_url,
			type: "POST",
			data: jsonData,
			success:function(data) {
					console.log('map added!');	
					console.log(data); 
					inputToAdd.resource_uri=ko.observable(postURL_input.getResponseHeader('location'));
					inputToAdd.id = inputToAdd.resource_uri().match(/\/mapelement\/(.*)\//)[1];
					VM.mapelements.push(inputToAdd); 
				},
			contentType: "application/json",
			});
	} 




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



