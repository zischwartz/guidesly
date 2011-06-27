
/////////////////////////////////////////////////////////////////////////////
///  Slide transition code  /////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////////////////

$(function() {
    if (typeof history.pushState === 'undefined') {
        alert("Warning -- your browser doesn't support HTML 5");
    } else {
        rebindSlideTransitionLinks();
    }
});

var _jqSlideFrameId = "DIV.slide";

// jQuery binding to replace the click() event on
// a link inside the slide frame.
function rebindSlideTransitionLinks() {
    $(_jqSlideFrameId+" A").click(function(event) {
        event.preventDefault();

        var url = this.href;
        history.pushState({path: url}, '', url);
        slideToUrl(url, true);
    });
}

// The purpose of this function is to do a slide
// transition between the div that's currently in
// the DOM and the jqNewDiv argument (which is a
// jQuery wrapper for the new div object,
// which has not yet been added to the DOM).
//
// goForward is a boolean indicating whether this
// is a forward transition (i.e. when a user clicks
// on a link) or a backward transition (i.e. when
// the user clicks the back button in the browser)
function slideTo(jqNewDiv, goForward) {
    var parent = $(_jqSlideFrameId).parent();
    var callback = function() {
        parent.empty();
        parent.append(jqNewDiv);
        var newNode = parent.find(_jqSlideFrameId);
        newNode.hide();
        newNode.fadeIn(300);
        rebindSlideTransitionLinks();
    };

    if (goForward) {
//        $(_jqSlideFrame).animate({ left: +1000 }, 1000, 'linear', callback);
        $(_jqSlideFrameId).fadeOut(300, callback);
    } else {
//        $(_jqSlideFrame).animate({ left: -1000 }, 1000, 'linear', callback);
        $(_jqSlideFrameId).fadeOut(300, callback);
    }
}

// like slideTo(), but with a url argument instead
// of the already-fetched HTML.
function slideToUrl(url, goForward) {
    var callback = function(data) {
        var jqSlideFrame = $(data).find(_jqSlideFrameId);
        slideTo(jqSlideFrame, goForward);
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
        slideToUrl(location.pathname, false);
    }
    currentLocation = location.pathname;
});

/////////////////////////////////////////////////////////////////////////////
///  End slide transition code  /////////////////////////////////////////////
/////////////////////////////////////////////////////////////////////////////