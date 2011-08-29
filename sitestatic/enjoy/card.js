
var _jqCardFrameId = "DIV.card";


$(document).ready(function(){	



///  THUMBS /////////////////////////////////////////////////
    $("a.thumb").live('click', function(event) {
		$(".active_thumb").removeClass("active_thumb");
		$(this).addClass("active_thumb");
		event.preventDefault();
		var media_type = $(this).data("media_type");
        var url = this.href;
		
		if (media_type == 'image')
		{
			$(".primary_media").attr({ src: url});
		}
	
	}); //end thumbs
	
	//keydown back and forth
	$("body").keydown(function(event) {
		 if (event.keyCode == '39') 
			var url = $(".next a").addClass("pressed").attr('href');
		if (event.keyCode == '37')
			var url = $(".prev a").addClass("pressed").attr('href');
		if (url)
		{
			event.preventDefault();
		 	cardToUrl(url, true);
			history.pushState({path: url}, '', url);
		}
	});//end keydown

	
	activateTimers();


/////////////////////////////////////////////////////////////////////////////
///  Card transition code  /////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////////////////
    if (typeof history.pushState === 'undefined') {
        alert("Warning -- your browser doesn't support HTML 5");
    } else {
        // jQuery binding to replace the click() event on
        // a link inside the card frame.
        $(_jqCardFrameId+" A.goto").live('click', function(event) {
            event.preventDefault();

            var url = this.href;
            history.pushState({path: url}, '', url);
            cardToUrl(url, true);
			
        });
    }
	
}); //end docready



// The purpose of this function is to do a card
// transition between the div that's currently in
// the DOM and the jqNewDiv argument (which is a
// jQuery wrapper for the new div object,
// which has not yet been added to the DOM).
//
// goForward is a boolean indicating whether this
// is a forward transition (i.e. when a user clicks
// on a link) or a backward transition (i.e. when
// the user clicks the back button in the browser)
function cardTo(jqNewDiv, goForward) {
    var parent = $(_jqCardFrameId).parent();
    var callback = function() {
        parent.empty();
        parent.append(jqNewDiv);
        var newNode = parent.find(_jqCardFrameId);
        newNode.hide();
        newNode.fadeIn(300);
        newNode.show();
   	$( '.video-js' ).VideoJS();              
   
//	      $("#jquery_jplayer_1").jPlayer({
//	        ready: function () {
//	          $(this).jPlayer("setMedia", {
//	            m4v: "{{primary_media.file}}"
//	          });
//	        },  
//	        swfPath: "{{STATIC_URL}}js-libs/",
//	        supplied: "M4V"
//	      });

		activateTimers();
    };

//    if (goForward) {
//        $(_jqCardFrame).animate({ left: +1000 }, 1000, 'linear', callback);
//    } else {
//        $(_jqCardFrame).animate({ left: -1000 }, 1000, 'linear', callback);
//    }
    $(_jqCardFrameId).fadeOut(300, callback);
}

// like cardTo(), but with a url argument instead
// of the already-fetched HTML.
function cardToUrl(url, goForward) {
    var callback = function(data) {
        var jqCardFrame = $(data).find(_jqCardFrameId);
        cardTo(jqCardFrame, goForward);

    };
    $.get(url, null, callback, "html");
}

// Keep track of the location (url) of the current page
var currentLocation = null;

// 'popstate' is the event called when an element
// is popped off the history stack (i.e. when the user
// presses the 'back' button).  It's also called, at least
// in Chrome, when the page is first displayed.
$(window).bind('popstate', function(event) {
    if (currentLocation != null) {
        cardToUrl(location.pathname, false);
    }
    currentLocation = location.pathname;
});

/////////////////////////////////////////////////////////////////////////////
///  End card transition code  /////////////////////////////////////////////
/////////////////////////////////////////////////////////////////////////////





function activateTimers(){
	$("a.timer").each(function(index) {
		var seconds = $(this).data("seconds") + $(this).data("minutes")*60 ;
		var timeBar = $("<div class='timeBar'></div>");
		$(this).append(timeBar);
		var timer_link = $(this);
		$(timeBar).animate({
		    width: 0
		  }, seconds*1000, function() {
		    // Animation complete.
			var url = $(timer_link).attr('href');
			cardToUrl(url, true);
			history.pushState({path: url}, '', url);
		  });
	}); //end timer	
	
}

