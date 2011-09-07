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

	VM.pmcid = ko.observable(); //primary_media_client_id

	//give all the existing elements a client_id, existing tag, and set their display stuff to external if it is
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
			
			//if this element has the same r-uri as the primary media, assign pmcid
			if (element.resource_uri() == VM.primary_media())
			{
				VM.pmcid(element.client_id());
			}
			
	}); //end each
	

	VM.check_if_primary = function(element)
	{
		if (element.client_id() == VM.pmcid())
			return true;
		else
			return false;
	}

	VM.makePrimary = function(element)
	{
		VM.pmcid(this.client_id());
		if (this.resource_uri())
			VM.primary_media(this.resource_uri());
	}
	
	
		

// **************************************
// ******      File Upload Plugin    ****
// **************************************

	$('#fileupload').fileupload({
	// options
		autoUpload: true,
		previewMaxWidth: 500,
		previewMaxHeight: 500
		// uploadTemplate: $('#mediaTemplate')
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
			        console.log('Added file: ' + file.name);
					console.log(file)
					
					var el = new Object();
					el.title = ko.observable(); //ko.observable(file.name.split('.')[0]);
					el.file_url = ko.observable();
					el.type = ko.observable(file.type.split('/')[0]);
					el.client_id = ko.observable('media' + file.name.split('.')[0].split(' ')[0] + file.size);
					el.card= VM.resource_uri();
					el.resource_uri= ko.observable();
					el.external_file= ko.observable();
					el.medium_url= ko.observable();
					
					//add it to the array
					VM.mediaelements.push(el);
					
					//if it's the first item, make it primary
					if 	(VM.mediaelements().length ==1)
						VM.pmcid(el.client_id());
						
					var the_element_jq= $("#"+ el.client_id());				
					the_element_jq.addClass("uploading");
					
					if (el.type() =='image')
					{
						$('#fileupload').data('fileupload')._loadImage(file, function (img) {
		                    // console.log(img.src);
							el.medium_url(img.src);
							// $(id_string).find('.preview_image').attr("src", img.src).fadeIn();
							// $(img).clone().hide().prependTo($(id_string).find('.preview_wrapper')).fadeIn().attr("class", "preview_image");
							}, //end callback
							$('#fileupload').fileupload('option') ); //end _loadimage
					}
					else
					{
						img = $("<img src='/static/img/upload-icon.png'/>");
					    $(img).hide().prependTo(the_element_jq.find('.preview')).fadeIn().attr("class", "preview_image");	
					}
					
				}); //end each	
				// console.log(data);
	}).bind('fileuploaddone',
		function (e, data) {

			$(this).css({backgroundColor: "#ffffff"});
			console.log('done uploading!');
			
			//File has been uploaded, now lets associated it with what's actually on the server.
			$.each(data.files, function (index, file) {
				
				var client_id = 'media' + file.name.split('.')[0].split(' ')[0] + file.size;

				var the_element_jq= $("#" + client_id);
				
				var the_element_ko = ko.utils.arrayFirst(VM.mediaelements(), function(item) { return item.client_id() === client_id;})
				the_element_ko.file_url(data.result[0].url);
				the_element_ko.resource_uri(media_api_url + data.result[0].id + '/');
				the_element_ko.medium_url(data.result[0].medium_image_url);
				
				the_element_jq.removeClass('uploading');
				
				//set the primary media here 
				if 	(VM.mediaelements().length ==1)
				{
					VM.primary_media(the_element_ko.resource_uri());
					VM.save_card();
				}
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
		console.log('this');
		console.log(this);
		var that = cleanClientStuff(this);
		console.log(that);
		
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

		var jsData = ko.mapping.toJS(VM);
		// if (VM.primary_media())
		// 	jsData.primary_media= VM.primary_media();
		delete jsData.mediaelements;
		jsonData = ko.toJSON(jsData);

		
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
	} // end aviary
	
//**********************************************
//******  INPUT AND INTERACTION ADDING     *****
// *********************************************
	VM.current_input_type= ko.observable();
	VM.current_input_verb= ko.observable();
	VM.newCardTitle= ko.observable();
	VM.newButtonText= ko.observable();
	VM.newActionGotoCard = ko.observable();
	VM.newTimerSeconds = ko.observable(00)
	VM.newTimerMinutes = ko.observable(00)


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
	inputToAdd.type= ko.observable(VM.current_input_type());
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
		VM.current_input_type('');
	
	} //end input adding functione



cleanClientStuff = function(that)
{
	delete that.file_url;
	delete that.client_id;
	delete that.existing;
	delete that.medium_url;
	delete that.file;
	delete that.doesnotexistthing;
	return that;
}


(function(a){a.fn.autoResize=function(j){var b=a.extend({onResize:function(){},animate:true,animateDuration:150,animateCallback:function(){},extraSpace:20,limit:1000},j);this.filter('textarea').each(function(){var c=a(this).css({resize:'none','overflow-y':'hidden'}),k=c.height(),f=(function(){var l=['height','width','lineHeight','textDecoration','letterSpacing'],h={};a.each(l,function(d,e){h[e]=c.css(e)});return c.clone().removeAttr('id').removeAttr('name').css({position:'absolute',top:0,left:-9999}).css(h).attr('tabIndex','-1').insertBefore(c)})(),i=null,g=function(){f.height(0).val(a(this).val()).scrollTop(10000);var d=Math.max(f.scrollTop(),k)+b.extraSpace,e=a(this).add(f);if(i===d){return}i=d;if(d>=b.limit){a(this).css('overflow-y','');return}b.onResize.call(this);b.animate&&c.css('display')==='block'?e.stop().animate({height:d},b.animateDuration,b.animateCallback):e.height(d)};c.unbind('.dynSiz').bind('keyup.dynSiz',g).bind('keydown.dynSiz',g).bind('change.dynSiz',g)});return this}})(jQuery);
