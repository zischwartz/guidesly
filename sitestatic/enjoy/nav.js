

$(function() {

// Nav animation
var container = $( "#bottom_nav" );
var tag = $("#tag");
container.hide();
tag.click(
function( event ){

if (container.is( ":visible" )){
	container.hide("slide", { direction: "left" }, 1000, function(){
	container.clearQueue();
	tag.switchClass('tag_expand','tag',75,'easeOutBounce');
	
});
} else {
	
	tag.switchClass('tag','tag_expand',100,'easeOutBounce', function(){
	container.clearQueue();
	container.show("slide", { direction: "left" }, 1000);
	
});
	
}
}
) (jQuery);


// Media controls

$('#play').click(function() {	
$("player").play();
});

$('#pause').click(function() {
$("player").pause();
});



}); // End doc

