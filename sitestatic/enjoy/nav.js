

$(function() {



// Nav animation
var container = $( "#bottom_nav" );
container.hide();
$("#tag").click(
function( event ){
 
if (container.is( ":visible" )){
	container.slideUp( 200 );
} else {
	container.slideDown( 200 ); 
}
}
);




// Media controls

$('#play').click(function() {
	if ($('video').length ) {
		$("video").get(0).play();
	}else if ($('audio').length ) {
		$("audio").get(0).play();
		}
});

$('#pause').click(function() {
	if ($('video').length ) {
    	if($('video').prop('paused') == false){
			$("video").get(0).pause();
		}

	}else if ($('audio').length ) {
    	if($('audio').prop('paused') == false){
			$("audio").get(0).pause();
		}
	}
});

$('#mute_check').click(function() {
	if ($('video').length ) {
    	if($('video').prop('muted') == true){
			$('video').prop('muted', false);
			$("#mute").css('color','#FFFFFF');
			}
		else{
		$('video').prop('muted', true);
		$("#mute").css('color','#000000');
		}
	}else if ($('audio').length ){
		if($('audio').prop('muted') == true){
			$('audio').prop('muted', false);
			$("#mute").css('color','#FFFFFF');
			}
		else{
		$('audio').prop('muted', true);
		$("#mute").css('color','#000000');
		}
	}
});

	
// Decrease the volume
$('#vDown').click(function() {
	$("video").get(0).volume = $("video").get(0).volume - .1;	
	$('volume').html(volume);
});
// Raise the volume
$('#vUp').click(function() {	
	$("video").get(0).volume = $("video").get(0).volume + .1;
	$('volume').html(volume);
});



}); // End doc

