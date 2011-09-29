var static_url = "/media/"  
//was /static/


var card_api_url='/api/v1/card/';
var media_api_url='/api/v1/mediaelement/';
var input_api_url='/api/v1/inputelement/';
var map_api_url='/api/v1/mapelement/';
var action_api_url='/api/v1/action/';
var file_api_url='/api/v1/userfile/';
var guide_api_url='/api/v1/guide/';
var timer_api_url='/api/v1/timer/';
var smallcard_api_url='/api/v1/smallcard/';

var VM; //our main viewmodel

var InputVM;

var initial_card_object;
var mapping;



// ***********************************************
// ***********       DOCREAD         *************
// ***********************************************
$(document).ready(function(){	

// Make stuff pretty
	jQuery.easing.def = "easeOutQuart";

$(".adder").hover(
	function(){
		$(this).addClass("hovered");
		$(this).doTimeout('hov'); //cancels the timer
	},
	function(){	$(this).doTimeout('hov', 4000, function(){this.removeClass("hovered");});	}	);
	
$(".mediaTemplate").live("mouseover mouseout", function(event) {
	  if ( event.type == "mouseover" ) {
		$(this).addClass("hovered");
		$(this).doTimeout('hov'); //cancels the timer
	  } else {
		$(this).doTimeout('hov', 2000, function(){this.removeClass("hovered");})
	  }
	});



//Prep inital data for card that's been saved previously and has existing
	initial_card_object= jQuery.parseJSON(initial_card_json);
	VM = ko.mapping.fromJS(initial_card_object);

	VM.pmcid = ko.observable(); //primary_media_client_id
	VM.has_audio_or_video = ko.observable(); 

	//give all the existing elements a client_id, existing tag, and set their display stuff to external if it is
	$.each(VM.mediaelements(), function (index, element) {

			element.client_id = ko.observable('media'+ element.id());
			element.existing = ko.observable(true);

			if (element.external_file())
			{
				element.file_url = ko.observable(element.external_file());
				element.medium_url = ko.observable(element.external_file());
				element.thumb_url = ko.observable(element.external_file());
			}
			else
			{
				element.file_url = ko.observable(element.file.display_url());
				element.medium_url = ko.observable(element.file.medium_url());
				element.thumb_url = ko.observable(element.file.thumb_url());
			}
			
			//if this element has the same r-uri as the primary media, assign pmcid
			if (element.resource_uri() == VM.primary_media())
			{
				//set the pmcid 
				VM.pmcid(element.client_id());
				//and sort the array
				if 	(VM.mediaelements().length > 1)
				{
					//sort the array and make the primary first
					VM.mediaelements.sort(function(left, right) {
				 		if (left.resource_uri() == VM.primary_media())
							return -1;
						else if (right.resource_uri() == VM.primary_media())
							return 1;
						else
							return 0;
					});
				}
			}//end element = primary
			
	}); //end each
	
	VM.saving_message = ko.observable();
	
	

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
		
		//if there's more than one element
		if 	(VM.mediaelements().length > 1)
		{
			//sort the array and make the primary first
			VM.mediaelements.sort(function(left, right) {
		 		if (left.client_id() == VM.pmcid())
					return -1;
				else if (right.client_id() == VM.pmcid())
					return 1;
				else
					return 0;
			});
		}
		VM.save_card();
	} //end makePrimary
	
	
		

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
			        // console.log('Added file: ' + file.name);
					// console.log(file);
					
					var el = new Object();
					el.title = ko.observable(file.name.split('.')[0]); //open question as to whether this should default to blank or the file name
					el.file_url = ko.observable();
					el.type = ko.observable(file.type.split('/')[0]);
					if ((el.type() != 'image') && (el.type() != 'video') && (el.type() != 'audio'))
						el.type('other');
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
					// else if (el.type() == 'video') 
					// 	VM.pmcid(el.client_id());
					
						
					var the_element_jq= $("#"+ el.client_id());			
					the_element_jq.addClass("uploading");
					
					if (el.type() =='image')
					{
						$('#fileupload').data('fileupload')._loadImage(file, function (img) {
		                    // console.log(img.src);
							el.medium_url(img.src);
							
							}, //end callback
							$('#fileupload').fileupload('option') ); //end _loadimage
					}
					else
					{
						the_element_jq.find(".preview").addClass("media_standin").addClass(el.type());
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
				
				the_element_jq.removeClass('uploading'); //.find('.fake_preview').slideUp().remove();
				
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


	// Save Generic Element, from implied KO event. See also save_this_element() below, which you pass the element to be saved. 
	VM.save_element = function()
	{

		if (this.type())
			VM.saving_message('Saving ' + this.type());
		else
			VM.saving_message('Saving!');
		
		var that = this; //cleanClientStuff(this);
		
		var jsonData = ko.mapping.toJSON(that);
		$.ajax({
			url: that.resource_uri(),
			type: "PUT",
			data:jsonData,
			success:function(data) { 
				if (that.type())
					VM.saving_message('Saved ' + that.type());
				else
					VM.saving_message('Save!');
				$.doTimeout('saved', 1000, function(){VM.saving_message('')}); 				
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
		VM.saving_message('Saving Card!');
		var jsData = ko.mapping.toJS(VM);
		// if (VM.primary_media())
		// 	jsData.primary_media= VM.primary_media();
		delete jsData.mediaelements;
		jsonData = ko.toJSON(jsData);

		
		$.ajax({
			url: VM.resource_uri(),
			type: "PUT",
			data:jsonData,
			success:function(data) { console.log(data); 
				VM.saving_message('Saved Card!');
				$.doTimeout('saved', 1000, function(){VM.saving_message('')}); },
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
	VM.current_input_type= ko.observable('');
	VM.current_input_verb= ko.observable();
	VM.newCardTitle= ko.observable('');

	VM.showInputModal = function()
	{	
		// console.log('this:');
		console.log('showInputModal');
		console.log(this);
		
		el=$('event.currentTarget');
		el=$(event.currentTarget);
		input_type = el.data("input_type");
		input_verb = el.data("input_verb");
		VM.InputVM().type(input_type);
		VM.current_input_verb(input_verb);
		
		if (input_verb == 'add')
			{
				// console.log('input verb was add, adding a new input');
				VM.InputVM(new anInput(input_type));
				VM.InputVM().save_element = function(){
					if (VM.InputVM().default_action.goto()=="addcard")
						addCardFromInput(this); //this needs to handle the rest
					else
						addInputHelper(this);
					
						$('#inputModal').modal('hide');
						
					
				}
			}
		if (input_verb == 'edit')
			{
				// console.log('input verb was edit, editing an old input');
				VM.InputVM(this); //assign the inputvm to the clicked element
				VM.InputVM().save_element = function(){
					if (VM.InputVM().default_action.goto()=="addcard")
						addCardFromInput(this); //this needs to handle the rest
					else
						addInputHelper(this);
						$('#inputModal').modal('hide');
						
					}; //end save element
			}
		$('#inputModal').modal({
			show:true,
			backdrop:true,
			keyboard:true,
			});
			
	}


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

	var converter = Markdown.getSanitizingConverter();
	var editor = new Markdown.Editor(converter);
	editor.run();
	
	$(".adder .closer").click(function(event){
		adder= $(this).parent();
		adder.addClass("minimized").removeClass('editing');
		event.stopPropagation();
		if (adder.hasClass('title'))
			VM.title('');
		return (false);
	});
	
	$(".modal .closer").click(function(event){
		$(this).parents('.modal').modal('hide')
	});
	

	$(".adder.minimized").live('click', function(){
		$(this).removeClass('minimized');
	});
		
	
	$(".delete_link").live('click',function(event){
		$(this).parent().addClass('confirm_delete');
		event.preventDefault();

	});
	
	$("#markdownhelpbutton").click(function(){
		is_displayed = $("#markdownhelp").css('display');
		console.log(is_displayed);
		if (is_displayed == 'none')
			$("#markdownhelp").slideDown();
		else
			$("#markdownhelp").slideUp();
	});
	
	
	
	// MEDIA ADDING, from external resources, or stuff user already uploaded
	VM.external_media_url = ko.observable('');
	VM.media_type_to_add = ko.observable('image');
	
	VM.addMedia = function (element) {
		var el = new Object();
		el.title = ko.observable('')
		el.file_url = ko.observable();
		el.type = ko.observable(VM.media_type_to_add());
		// el.client_id = ko.observable('media' + file.name.split('.')[0].split(' ')[0] + file.size);
		el.card= VM.resource_uri();
		el.external_file= ko.observable(VM.external_media_url());
		el.medium_url= ko.observable(VM.external_media_url());
		
		
		jsonData = ko.toJSON(el); 	// console.log(jsonData);
		postURL_input=$.ajax({
			url: media_api_url,
			type: "POST",
			data: jsonData,
			success:function(data) {
				el.resource_uri=ko.observable(postURL_input.getResponseHeader('location'));
				el.id = el.resource_uri().match(/\/mediaelement\/(.*)\//)[1];
				el.client_id = ko.observable('media'+ el.id);
				VM.mediaelements.push(el); 
				//if it's the first item, make it primary
				if 	(VM.mediaelements().length ==1)
					VM.pmcid(el.client_id());
					
				$('#addExternalMediaModal').modal('hide');
				
				VM.save_card();
				},
			contentType: "application/json",
			});
		
		
		
		// VM.mediaelements.push(el);
		

	}
	
	

	//REPLACE CARDS WITH GUIDE TODO because guide has the relevant info about each card anyway
	initial_guide_object= jQuery.parseJSON(guide_json);
	
	
	VM.all_cards = ko.observableArray();
	for (x in initial_guide_object.cards)
		{
			VM.all_cards.push(initial_guide_object.cards[x]);
		}


	VM.InputVM= ko.observable(new anInput());
	
	ko.applyBindings(VM);





});// end docreadyy ---  end docreadyy ---  end docreadyy ---  end docreadyy ---  end docreadyy 
// end docreadyy ---  end docreadyy ---  end docreadyy ---  end docreadyy ---  end docreadyy 


// HEEEEEEEEEEEEEEEEELLLLLLLLLLLLLLLLLLLLLLLLLLPPPPPPPPPPPPPPPPPPPEEEEEERRRRRRRRRRRRRRRRRRRs


var anInput = function(type) {
	
	var default_action = new Object();
	default_action.goto = ko.observable();
	default_action.id = null;
	
    this.type = ko.observable(type);
    this.card = ko.observable(VM.resource_uri());
    this.button_text= ko.observable();
    this.resource_uri=ko.observable();

	this.default_action= default_action;
    this.newCardTitle=ko.observable();

	if (type == 'timer')
		{
			this.seconds= ko.observable(0);
			this.minutes= ko.observable(0);
		}

}

// BUG TODO , inputs with new cards don't show as selecting the new card/action  until you refresh the page.
// when you click on it, the VM.InputVM().default_action.goto() is a function, need additional (), not sure where that's being introduced

addInputHelper =function(that){
	var postURL_input;
	
	if (that.resource_uri()) //if it has a resource uri, it exists, and should be put
	{
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
	
	else  //otherwise it's new
	{
		jsonData = ko.toJSON(that); 	// console.log(jsonData);
		postURL_input=$.ajax({
			url: input_api_url,
			type: "POST",
			data: jsonData,
			success:function(data) {
				that.resource_uri=ko.observable(postURL_input.getResponseHeader('location'));
				that.id = that.resource_uri().match(/\/inputelement\/(.*)\//)[1];
				VM.inputelements.push(that); 
				},
			contentType: "application/json",
			});
	}
	

		
	
	} //end input adding function

addCardFromInput = function(that)
{
	
	console.log('addcarding');
	cardToAdd= new Object();
	cardToAdd.title= VM.newCardTitle();			
	cardToAdd.guide= VM.guide();
	var postURL_newcard;
	jsonData = ko.toJSON(cardToAdd);
	console.log(jsonData);
	postURL_newcard=$.ajax({
		url: smallcard_api_url,
		type: "POST",
		data: jsonData,
		success:function(data) {
			console.log('success creating a new card');
			// console.log(postURL_newcard.getResponseHeader('content-location'));
			new_card_uri= postURL_newcard.getResponseHeader('location');
			uri_string_n=new_card_uri.indexOf('api');
			new_card_uri= new_card_uri.slice(uri_string_n-1);
			console.log(new_card_uri);
			cardToAdd.resource_uri=ko.observable(new_card_uri);
			cardToAdd.id = cardToAdd.resource_uri().match(/\/smallcard\/(.*)\//)[1];
			cardToAdd.edit_url = '/create/' + guide_slug + '/' + cardToAdd.id + '/';
			cardToAdd.absolute_url = '/i/' + cardToAdd.id + '/'
			//guide_slug is defined in the html document, and the absolute id is a redirect based on the id...
			VM.all_cards.push(cardToAdd);
			VM.InputVM().default_action.goto(cardToAdd.resource_uri());
			addInputHelper(VM.InputVM());
			VM.newCardTitle('');
		},
	contentType: "application/json",	
	});

}


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


var deleteCard= function(event)
{
	// console.log(event.target.parents(".smallcardWrapper"));
	
	if (typeof(this.resource_uri) == 'function')
		{
			this_uri= this.resource_uri();
			this_id = this.id();
		}
	else
		{
			this_uri= this.resource_uri;
			this_id = this.id;	
		}
	
	$.ajax({
		url: this_uri,
		type: "DELETE",
		success:function(data) { console.log(data); },
		contentType: "application/json",
	});
	
	if (parseInt(this_id, 10) == VM.id())
		window.location = edit_guide_url;

		VM.all_cards.remove(this);
};


function didPressEnter(event)
{if ( event.which == 13 )
		{
			turnOffEditing(event);
		}
	return (true);}

function turnOnEditing(event)
{	
	console.log('turnOnEditing');
	el=$(event.currentTarget);
	el.addClass('editing');
	el.find("textarea:first").focus();
	el.find("input:first").focus();
	event.stopPropagation();
	return false;
}

function turnOffEditing(event)
{
	el=$(event.target);
	console.log(el.hasClass('editing'));
	console.log(el);
	if (el.hasClass('editing'))
	{
		event.stopPropagation();
		return false;
	}
	$(el).removeClass('editing');
	$(el).parents('.editing').removeClass('editing');
	$("#markdownhelp").hide();

	event.stopPropagation();
	VM.save_card();
}

function save_this_element(element)
{


	if (element.type())
		VM.saving_message('Saving ' + element.type());
	else
		VM.saving_message('Saving!');
	
	
	var jsonData = ko.mapping.toJSON(element);
	$.ajax({
		url: element.resource_uri(),
		type: "PUT",
		data:jsonData,
		success:function(data) { 
			if (element.type())
				VM.saving_message('Saved ' + element.type());
			else
				VM.saving_message('Save!');
			$.doTimeout('saved', 1000, function(){VM.saving_message('')}); 				
			console.log(data); 
			},
		contentType: "application/json",
		});
}



(function($){var a={},c="doTimeout",d=Array.prototype.slice;$[c]=function(){return b.apply(window,[0].concat(d.call(arguments)))};$.fn[c]=function(){var f=d.call(arguments),e=b.apply(this,[c+f[0]].concat(f));return typeof f[0]==="number"||typeof f[1]==="number"?this:e};function b(l){var m=this,h,k={},g=l?$.fn:$,n=arguments,i=4,f=n[1],j=n[2],p=n[3];if(typeof f!=="string"){i--;f=l=0;j=n[1];p=n[2]}if(l){h=m.eq(0);h.data(l,k=h.data(l)||{})}else{if(f){k=a[f]||(a[f]={})}}k.id&&clearTimeout(k.id);delete k.id;function e(){if(l){h.removeData(l)}else{if(f){delete a[f]}}}function o(){k.id=setTimeout(function(){k.fn()},j)}if(p){k.fn=function(q){if(typeof p==="string"){p=g[p]}p.apply(m,d.call(n,i))===true&&!q?o():e()};o()}else{if(k.fn){j===undefined?e():k.fn(j===false);return true}else{e()}}}})(jQuery);
