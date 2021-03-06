var static_url = "/media/"  
//was /static/


var card_api_url='/api/v1/card/';
var media_api_url='/api/v1/mediaelement/';
var input_api_url='/api/v1/inputelement/';
var map_api_url='/api/v1/mappoelement/';
var action_api_url='/api/v1/action/';
var file_api_url='/api/v1/userfile/';
var guide_api_url='/api/v1/guide/';
// var timer_api_url='/api/v1/timer/';
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



	// map existing inputelements to our js model (with dependent observables etc) woo constructors
	var mapping = {
	    'inputelements': {
	        create: function(options) {
	            return new anInput(options.data);
	        }
	    }
	}

//Prep inital data for card that's been saved previously and has existing

	initial_card_object= jQuery.parseJSON(initial_card_json);
	
	VM = ko.mapping.fromJS(initial_card_object, mapping);

	VM.pmcid = ko.observable(); //primary_media_client_id
	VM.has_audio_or_video = ko.observable(); 
	VM.saving_message = ko.observable();
	VM.hasMap =  ko.observable(); 
	VM.draggable =  ko.observable(0); 
	
	
//FOR MEDIA ELEMENTS.
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
			
	}); //end each for media elements	
	

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
	
// FOR INPUTELEMENTS

$.each(VM.inputelements(), function (index, element) {
	
	if (element.type()=='timer')
		element.formattedtime = ko.dependentObservable(function() {
			// return 'hello';
			console.log(this);
			return timerFormat(this.minutes(), this.seconds());
		}, element);
		
	if (element.type() == 'place')
	{
		VM.hasMap(1);
		// initialize_map();
	}	

})
		

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
	
	
	VM.addingPointByHand= ko.observable(); 
	VM.address= ko.observable(); 
	VM.mapError= ko.observable(); 

	VM.showInputModal = function()
	{	

		// console.log('showInputModal');
		// console.log(this);
		
		// el=$('event.currentTarget');
		el=$(event.currentTarget);
		
		var ko_el_clicked = true; //because we're allowing two ways to click mappoints
		
		
		//check if this is normal input or a mappoint
		if (el.data("input_type"))
		{
			input_type = el.data("input_type");
			input_verb = el.data("input_verb");
			VM.current_input_verb(input_verb);
		}
		//it's a mappoint
		else
		{
			//we'll just assume 
			input_type = "place";
			input_verb = 'edit'
			VM.current_input_verb(input_verb);
			ko_el_clicked = false;
		}

		
		if (input_verb == 'add')
			{
				// console.log('input verb was add, adding a new input');
				if (input_type == 'map')
				{
					VM.hasMap('True');
					initialize_map();
					return true;
				}
				
				VM.InputVM(new anInput({"type":input_type}));

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
				
				//for places clicked on the map, we're assigning it to the InputVM earlier. Otherwise assign it here.
				if (input_type != "place" || ko_el_clicked)  
					VM.InputVM(this); //assign the inputvm to the clicked element
					
					
				VM.InputVM().save_element = function(){
					if (VM.InputVM().default_action.goto()=="addcard")
						addCardFromInput(this); //this needs to handle the rest
					else
						addInputHelper(this);
					if (input_type== "place")
						this.stop_bouncing();
					
					$('#inputModal').modal('hide');
						
					}; //end save element
			}
		$('#inputModal').modal({
			show:true,
			backdrop:true,
			keyboard:true,
			});
			
			// .bind('shown', function () {
			// 	 if (map)
			// 		{
			// 			google.maps.event.trigger(map, "resize");
			// 			// map.setCenter(map.getCenter());
			// 			// map.setZoom( map.getZoom() );
			// 		}
			// });
			
	}

	//for media elements.
	VM.deleteFromCard= function()
	{
		console.log("yess lets delete this:");
		console.log(this.resource_uri());
		
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

	};
	

	VM.inputTypeTemplate= function(element){
		console.log(element);
	
			if (element.type()=="button")
				return 'buttonTemplate';
			if (element.type() == 'timer')
				return 'timerTemplate';
			if (element.type() == 'place')
				return 'mapTemplate';
			else			
				return 'errorNoTemplate';
	}
	
	
	VM.inputsNotPlaces = ko.dependentObservable(function () {      
	    return ko.utils.arrayFilter(this.inputelements(), function(el) {
	        return el.type() != 'place';
	    });
	}.bind(VM));
	
	VM.justPlaces = ko.dependentObservable(function () {      
	    return ko.utils.arrayFilter(this.inputelements(), function(el) {
	        return el.type() == 'place' ;
	    });
	}.bind(VM));
	

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
	
	data = {};
	VM.InputVM= ko.observable(new anInput(data));
	
	ko.applyBindings(VM);

	



});// end docreadyy ---  end docreadyy ---  end docreadyy ---  end docreadyy ---  end docreadyy 
// end docreadyy ---  end docreadyy ---  end docreadyy ---  end docreadyy ---  end docreadyy 


// HEEEEEEEEEEEEEEEEELLLLLLLLLLLLLLLLLLLLLLLLLLPPPPPPPPPPPPPPPPPPPEEEEEERRRRRRRRRRRRRRRRRRRs

// var testmarker;

function anInput (data) {
	
	console.log('data');
	console.log(data);
	var default_action = new Object();
	// default_action.goto = ko.observable(data.default_action.goto || '');
	if (typeof data.default_action !='undefined')
	{	default_action.goto = ko.observable(data.default_action.goto);
		default_action.id = data.default_action.id;	
	}
	else
	{	default_action.goto = ko.observable();
		default_action.id =  null;	
	}
	
	var that =this;
    this.type = ko.observable(data.type || '');
    this.card = ko.observable(initial_card_object.resource_uri);
    this.button_text= ko.observable(data.button_text || '');
    this.sub_title= ko.observable(data.sub_title || '');
    this.resource_uri=ko.observable(data.resource_uri || '');

	this.default_action= default_action ;
    this.newCardTitle=ko.observable();

	this.execute_action_when_done = ko.observable( data.execute_action_when_done || 'true');

	if (data.type=='place')
	{
		if (!map)
			initialize_map();

		this.lat= ko.observable(data.lat);  //these really should never be blank
		this['long']= ko.observable(data['long']);
		this.manual_addy =ko.observable(data.manual_addy || '');
	  
		var marker = new google.maps.Marker({
		        position: new google.maps.LatLng(data.lat, data.long),
		        title: data.button_text || 'Your Place',
		        map: map,
				animation: this.button_text() ? null: google.maps.Animation.BOUNCE,
		        // draggable: true
		    });
		
		all_markers_bounds.extend(marker.position);
		
		 var boxText = document.createElement("div");	

		 // boxText.innerHTML = "<div class='twipsy-arrow'></div><div class='twipsy-inner'>"+ marker.title +"</div>";
		 t = this.button_text() ? this.button_text() : 'Click to edit';
		 boxText.innerHTML = "<div class='twipsy-arrow'></div><div class='twipsy-inner'>"+ t +"</div>";
		
		 var infoBoxOptions = {
		                 content: boxText
		                ,disableAutoPan: false
		                // ,maxWidth: "250px"
						,alignBottom: true
						,boxClass: 'twipsy fade above in'
		                // ,pixelOffset: new google.maps.Size(15, -40)
		                ,pixelOffset: new google.maps.Size(-55, -35) 
		                ,closeBoxURL: ""
		                // ,infoBoxClearance: new google.maps.Size(1, 1)
		                ,pane: "floatPane"
		                ,enableEventPropagation: false
						,boxStyle: { 
						                  opacity: 0.75
						                  // ,minWidth: "50px"
						                  ,width: "100px"
						                  // ,width: "auto"
						                 }
		        };
		
	    var ib = new InfoBox(infoBoxOptions);
		ib.open(map, marker);
	    
	
		//theres a bug here, this isn't called when the text changes. maybe make this binding live
		$(boxText).click(function(){
			console.log('infoboxclicked');
			VM.InputVM(that);
			VM.showInputModal();
		});
		
		this.button_text.subscribe(function(newValue) {
			boxText.innerHTML = "<div class='twipsy-arrow'></div><div class='twipsy-inner'>"+ that.button_text()  +"</div>";
		 
				// ib.setContent("<div class='twipsy-arrow'></div><div class='twipsy-inner'>"+ that.button_text() +"</div>");
			});
		
		google.maps.event.addListener(marker, 'click', function() {
				if (!VM.draggable())
				{
					VM.InputVM(this);
					VM.showInputModal();
				}
		    }.bind(this));
		
		
	    google.maps.event.addListener(marker, 'dragend', function() {
	        var pos = marker.getPosition();
	        this.lat(pos.lat());
	        this.long(pos.lng());
			save_this_element(this);
	    }.bind(this));
		
		this.delete_marker = function(){
			marker.setMap(null);
			ib.close();
		};
		
		this.stop_bouncing = function(){
			marker.setAnimation(null);
		};
		
		this.make_dragable = function(){
			marker.setDraggable(true);
		};
		
		this.stop_draggable = function(){
			marker.setDraggable(null);
		};

	}
	
	if (data.type == 'timer')
		{
			this.seconds= ko.observable(data.seconds || 0);
			this.minutes= ko.observable(data.minutes || 0);
			this.formattedtime = ko.dependentObservable(function() {
				return timerFormat(this.minutes(), this.seconds());
			}, this);
			
			this.ding_when_done = ko.observable(data.ding_when_done || '');
			this.auto_start = ko.observable(data.auto_start || 'true');
			
			this.complete = ko.dependentObservable(function() {
				if (this.button_text())
					if (this.seconds() || this.minutes())
						if (!this.execute_action_when_done())
							return true;
						else
							if (this.default_action.goto())
								return true;
				return false;
			}, this);

		} //end if timer
	
	else  //if it's not a timer or map, this is the dO for completeness
	{	this.complete = ko.dependentObservable(function() {
			if (this.button_text() && this.default_action.goto())
				return true;
			else
				return false;
			}, this);
	} //end if not timer
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

function delete_this_element(element)
{
	console.log("lets delete THIS input");
	console.log(element);

	$.ajax({
		url: element.resource_uri(),
		type: "DELETE",
		success:function(data) { console.log(data); },
		contentType: "application/json",
	});

	if (VM.inputelements.indexOf(element)!=-1)
		VM.inputelements.remove(element);
		
	if (element.type()=='place')
	{
		element.delete_marker();
		
	}
}


(function($){var a={},c="doTimeout",d=Array.prototype.slice;$[c]=function(){return b.apply(window,[0].concat(d.call(arguments)))};$.fn[c]=function(){var f=d.call(arguments),e=b.apply(this,[c+f[0]].concat(f));return typeof f[0]==="number"||typeof f[1]==="number"?this:e};function b(l){var m=this,h,k={},g=l?$.fn:$,n=arguments,i=4,f=n[1],j=n[2],p=n[3];if(typeof f!=="string"){i--;f=l=0;j=n[1];p=n[2]}if(l){h=m.eq(0);h.data(l,k=h.data(l)||{})}else{if(f){k=a[f]||(a[f]={})}}k.id&&clearTimeout(k.id);delete k.id;function e(){if(l){h.removeData(l)}else{if(f){delete a[f]}}}function o(){k.id=setTimeout(function(){k.fn()},j)}if(p){k.fn=function(q){if(typeof p==="string"){p=g[p]}p.apply(m,d.call(n,i))===true&&!q?o():e()};o()}else{if(k.fn){j===undefined?e():k.fn(j===false);return true}else{e()}}}})(jQuery);



function timerFormat(minutes, seconds)
{
    var timestring =''; 
    
    if (minutes <10)
        timestring= '0' + minutes;
    else
        timestring= minutes;
    
    timestring+= ':'
    
    if (seconds <10)
        timestring+= '0' + seconds;
    else
        timestring+= seconds;

    return timestring;
      
}