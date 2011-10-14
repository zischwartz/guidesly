
var History = window.History;

// Bind to StateChange Event
History.Adapter.bind(window,'statechange',function(){ // Note: We are using statechange instead of popstate
    var State = History.getState(); // Note: We are using History.getState() instead of event.state
	// console.log('Statechange historyjs: ' + State.data.slug);
    // History.log(State.data, State.title, State.url);
	var index= $(".card").index( document.getElementById(State.data.slug));
	$.deck('go', index);
});

	


$(document).ready(function(){
	
	//Video Setup
	VideoJS.setupAllWhenReady();  
	
	//Initialize Deckjs
	$.deck('.card', { keys: {next: -1, previous: -1} }); // No key activation, we'll do our own
	
	//Go to previous/existing state
	var initialState = History.getState();
	var initialUrl = initialState.cleanUrl;
	// console.log(initialState);

	var splitUrl=initialUrl.split('/');

	if (splitUrl[splitUrl.length-1] == '')
		splitUrl.pop();

	initialSlug = splitUrl[splitUrl.length-1];


	// if it's got data.slug
	// var index= $(".card").index( document.getElementById(initialState.data.slug));
	var index= $(".card").index( document.getElementById(initialSlug));
	

	$.deck('go', index);
	
	//this needs to handle if there's no previous state, can't rely on data.slug
	// on / and make that the slug

	
	//set the TOC up with the current card, and the video player
	inital_card = $.deck('getSlide');
	current_card_slug = initialState.data.slug;
	
	//if owner, set edit url for first card
	edit_url= inital_card.find(".edit_card_link").attr('href');
	$("#editCard a").attr('href', edit_url);
	
	$("#header").find("a.goto[data-destination="+current_card_slug+"]").addClass("active");
	if (inital_card.data("autoplay"))
		$.doTimeout(300, function(){inital_card.find(".video-js").player().play();});
	
	setupTimers(inital_card);
	if (inital_card.hasClass('hasmap'))
		setupMap(inital_card)
	
	$("#header").hover(
		function(){
			$(this).addClass("hovered");
			$(this).doTimeout('showtoc'); //cancels the timer
		},
		function(){	
			$(this).doTimeout('showtoc', 1000, function(){this.removeClass("hovered");});	}	);



//Bind the keys for back and forward
	$(window).keydown(function(event) {
		if (event.keyCode == '39')
		{
			next_button= $.deck('getSlide').find('.prev_and_next .input_element.next');
			if (next_button.length)
				$.deck('next');
			event.preventDefault();
			return false;
		} //end 39
		
		if (event.keyCode == '37')
		{
			prev_button= $.deck('getSlide').find('.prev_and_next .input_element.prev');
			if (prev_button.length)
				$.deck('prev');
			event.preventDefault();
			return false;
		} //end 37
		
	}); //end keypress binding
	

// On Deck Change, ...change the title and update the toc, to all kinds of housekeeping.
	$(document).bind('deck.change', function(event, from, to) {	
		card = $.deck('getSlide', to);
		title = $(card).data("title");
		current_card_slug = $(card).data("slug");
		
		document.title = guide_title + ': '+ title;
		$("#header a.goto").removeClass("active");
		$("#header").find("a.goto[data-destination="+current_card_slug+"]").addClass("active");
		
		// History.js
		History.pushState({slug: current_card_slug } , title, current_card_slug);
		
		if (card.data("autoplay"))
			card.find(".video-js").player().play();
		
		//only matters if owner
		edit_url= card.find(".edit_card_link").attr('href');
		$("#editCard a").attr('href', edit_url);

		setupTimers(card);
		if (card.hasClass('hasmap'))
			setupMap(card)
		

	});

// Bind prev and next buttons to move the deck	
	$('.input_element.prev').click(function(event) { $.deck('prev'); return false;});
	$('.input_element.next').click(function(event) { $.deck('next'); return false;});
	
	
// Bind other input buttons to move deck	
	$('a.goto').click(function(event) {
		// console.log($.deck('getSlides'));
		destination= $(event.target).data("destination");
		index= $(".card").index( document.getElementById(destination));
		// console.log(index);
		$.deck('go', index);
		return false;
	}); //end a.goto click
	
	
// Bind media thumbnails to change the video or image in the appropriate card
    $("a.thumbLink").live('click', function(event) {
		event.preventDefault();
		
		if ($(this).hasClass("activeThumbLink"))
			return false;
		
		var card = $.deck('getSlide');	
		$(card).find(".activeThumbLink").removeClass("activeThumbLink");
		$(this).addClass("activeThumbLink");
		var thumb_media_type = $(this).data("media_type");
        var url = this.href;
		var media_title = this.title;
		
		card.find(".caption").text(media_title);

		if (thumb_media_type == 'image')
		{
			if (current_media_type == 'video')
			{
				console.log('do something here to hide the video and replace it with an image');
			}
			
			if (card.hasClass("primary_is_bg"))
				{
					$(card).css('background-image', "url("+ url +")" ).addClass("loading");
					$('<img/>').attr('src', url).load(function(){
						$(card).removeClass("loading");
					});
				}
			else
			{
				$(card).addClass("loading").find(".primary_media").attr({ src: url});
				// bind to hide the loading indicator .loader
				$(card).find(".primary_media").load(function(){
					$(card).removeClass("loading");
				});
			}
		}//end if thumb_media_type is 'image'
	}); //end thumbsnail code live

}); //end docreadyyyyyyyyyyyyyyyyyyyyyy

//Fix for weird firefox horizontal scroll issue
window.addEventListener('MozMousePixelScroll', function(evt){
    if(evt.axis === evt.HORIZONTAL_AXIS){
        evt.preventDefault();
    }
}, false);



function setupTimers(card){
	card.find(".timer").each(function(index) {
		timer= $(this);	
		$(timer).find(".timebar").width('100%');
		
		if (timer.data("auto_start") == 'False')
			{
				console.log('not auto starting, you gota click');
				timer.click(function(event){
					// console.log(this);
					activateTimer(timer);
					event.preventDefault();
					return false;
				});
				
				var seconds = timer.data("seconds") + timer.data("minutes")*60 ;
				timer.find('.time').html(timerFormat(seconds));
			} //autostart false
			
		else if (timer.data("auto_start") == 'True')
			activateTimer(timer);
	})	
} //end setup timer

function activateTimer(timer)
{
	if (timer.hasClass("active"))
		return false;
	else
		timer.addClass("active");
		
	console.log('timer active!');
	var seconds = $(timer).data("seconds") + $(timer).data("minutes")*60 ;
	var timebar = $(timer).find(".timebar");
	var seconds_passed=0;
		
	timer.unbind('click');
	timer.click(function(event){
		event.preventDefault();
		console.log('clickckckc');
		return false;
	});
	
	$(timer).doTimeout(1000, function(){
		seconds_passed+=1;		
		console.log(seconds_passed)
		this.find('.time').html(timerFormat(seconds-seconds_passed));
		if (seconds_passed >= seconds)
			{
				timer.unbind('click');
				timer.removeClass("active");
				
				// do stuff and then
				if (this.data("ding_when_done")=='True')
					alert('Time is up!');
				
				destination = this.data('destination');
				execute_action_when_done = (this.data('execute_action_when_done') == 'True') ;
				// console.log(execute_action_when_done);
				
				if (destination && execute_action_when_done)
				{
					console.log('going to:');
					console.log(destination);
					index= $(".card").index( document.getElementById(destination));
					$.deck('go', index);
					return false;
				}
					
				return false;
			}
		else
			return true; //which makes it keep looping/poll
	});
	
	// console.log(this);	
	$(timebar).animate({
	    width: 0
	  }, seconds*1000, function() {
	    // Animation complete.
		console.log('done');
	  });
} //end activateTimer
	


/*
 * jQuery doTimeout: Like setTimeout, but better! - v1.0 - 3/3/2010
 * http://benalman.com/projects/jquery-dotimeout-plugin/
 * 
 * Copyright (c) 2010 "Cowboy" Ben Alman
 * Dual licensed under the MIT and GPL licenses.
 * http://benalman.com/about/license/
 */
(function($){var a={},c="doTimeout",d=Array.prototype.slice;$[c]=function(){return b.apply(window,[0].concat(d.call(arguments)))};$.fn[c]=function(){var f=d.call(arguments),e=b.apply(this,[c+f[0]].concat(f));return typeof f[0]==="number"||typeof f[1]==="number"?this:e};function b(l){var m=this,h,k={},g=l?$.fn:$,n=arguments,i=4,f=n[1],j=n[2],p=n[3];if(typeof f!=="string"){i--;f=l=0;j=n[1];p=n[2]}if(l){h=m.eq(0);h.data(l,k=h.data(l)||{})}else{if(f){k=a[f]||(a[f]={})}}k.id&&clearTimeout(k.id);delete k.id;function e(){if(l){h.removeData(l)}else{if(f){delete a[f]}}}function o(){k.id=setTimeout(function(){k.fn()},j)}if(p){k.fn=function(q){if(typeof p==="string"){p=g[p]}p.apply(m,d.call(n,i))===true&&!q?o():e()};o()}else{if(k.fn){j===undefined?e():k.fn(j===false);return true}else{e()}}}})(jQuery);



function timerFormat(total_seconds)
{
	seconds= total_seconds % 60;

	total_seconds = total_seconds- seconds;
	
	minutes = total_seconds/60;
	
    var timestring ='-'; 
    if (minutes <10)
        timestring+= '0' + minutes;
    else
        timestring+= minutes;
    timestring+= ':'
    if (seconds <10)
        timestring+= '0' + seconds;
    else
        timestring+= seconds;
    return timestring;
}


function setupMap(card)
{
	var map;
	var placeArray = [];
	requested_card=jQuery.parseJSON(requested_card_json);

	var places = requested_card.inputelements.filter(function(element){ if (element.type=='place') return element;})
	 
	var map_canvas= card.find(".map_canvas")[0]
	
	// $('.poptarget').popover({
	// 	html: true,
	// 	// live: true,
	// 	fallback: 'FALLBACKz',
	// });
	
	// $('.poptarget').twipsy({
	// 	// live: true,
	// 	// placement: 'right',
	// 	fallback: 'FALLBACKz',
	// 	// trigger: 'manual'
	// });
	
	
	if (current_card_slug == requested_card.slug)
	{	
		//yo dawg, I heard you like callbacks.
		google.load("maps", "3", {'other_params':"sensor=false", callback: function(){
			$.getScript(STATIC_URL+ 'js-libs/infobox_packed.js', function(data, textStatus)
			{
				var first = new google.maps.LatLng(places[0]['lat'], places[0]['long']);
				var all_markers_bounds = new google.maps.LatLngBounds();


				var mapOptions = {
					zoom: 12,
					center: first,
					mapTypeId: google.maps.MapTypeId.ROADMAP,
					streetViewControl: false,
					zoomControl: true,
					zoomControlOptions: {
					style: google.maps.ZoomControlStyle.SMALL},
					scrollwheel: false, // ?
				};

			  	map =  new google.maps.Map(map_canvas, mapOptions);

				$.each(places, function(index, value){
					placeArray.push(new aPlace(this, map, all_markers_bounds));
				});

				map.fitBounds(all_markers_bounds);

				google.maps.event.addListener(map, 'tilesloaded', function(){ 
				       // alert('hi'); 
					$.each(placeArray, function(index, value){
						setTimeout(function() {
						      placeArray[index].add();
						    }, index * 300 + 200);
					});//end each	

					
				});//end tilesloaded

			}); // end getscript for infobox		
		 	
			
		}}); //end google load callback
		
		
	}//end if current card
	
	// http://127.0.0.1:8000/api/v1/inputelement/?format=json&card=14&type=place

}

function aPlace (data, map, all_markers_bounds)
{
	
	var marker = new google.maps.Marker({
	        position: new google.maps.LatLng(data.lat, data.long),
	        title: data.button_text || 'A Place',
	        // map: map,
			animation: google.maps.Animation.DROP,
	    });
	
	all_markers_bounds.extend(marker.position);
	
	google.maps.event.addListener(marker, 'click', function() {
		alert('clicked! ' + marker.title);
	    });
	    // }.bind(this));
	
	
	 var boxText = document.createElement("div");	

	 boxText.innerHTML = "<div class='poptarget' title=" + marker.title + " data-content=" + 'Lorem ipsum' + "> -- </div>";
	
	 var infoBoxOptions = {
	                 content: boxText
	                ,disableAutoPan: false
	                // ,maxWidth: "250px"
					// ,alignBottom: true
					,boxClass: 'ib'
					// ,boxClass: 'twipsy fade right in'
	                ,pixelOffset: new google.maps.Size(-20, -35)
	                // ,pixelOffset: new google.maps.Size(10, -30) 
	                // ,pixelOffset: new google.maps.Size(0,0) 
	                ,closeBoxURL: ""
	                // ,infoBoxClearance: new google.maps.Size(1, 1)
	                ,pane: "floatPane"
	                ,enableEventPropagation: false
					,boxStyle: { 
					                  opacity: 0.75
					                  // ,minWidth: "50px"
					                  // ,width: "100px"
					                  // ,width: "auto"
					                 }
	        };
	
    var ib = new InfoBox(infoBoxOptions);
	// console.log(ib);
	

	
	

	
	this.add = function()
	{
		marker.setMap(map);
		setTimeout(function() {
			ib.open(map, marker);
						
			// $('.poptarget').popover({
			// 	html: true,
			// 	// live: true,
			// 	fallback: 'FALLBACKz',
			// });
			// 
			// $('.poptarget').twipsy({
			// 	// live: true,
			// 	// placement: 'right',
			// 	fallback: 'FALLBACKz',
			// 	trigger: 'manual'
			// });
			// 
			// console.log($(boxText).find('.poptarget').get(0));
			// 
			// p=$(boxText).find('.poptarget').get(0);
			// $(p).twipsy('show');
			
			
		    },  200);	
	} //end add
	


} //end aPlace