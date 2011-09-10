

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
$("#jquery_jplayer_1").jPlayer("play");
});

$('#pause').click(function() {
$("#jquery_jplayer_1").jPlayer("pause");
});

$('#mute_check').click(function() {

    	if($("#jquery_jplayer_1").data("jPlayer").status.muted == true){
			$("#mute").css('color','#FFFFFF');
			$("#jquery_jplayer_1").jPlayer("unmute");
			}
		else{
		$("#jquery_jplayer_1").jPlayer("mute");
		$("#mute").css('color','#000000');
		}

}) (jQuery);

	
// Decrease the volume
$('#vDown').click(function() {
	var volume = $("#jquery_jplayer_1").data("jPlayer").status.volume 
	volume = volume - .1
    $("#jquery_jplayer_1").jPlayer("volume", volume); // 0.0 - 1.0
    $("#volumePercent").html(newValue);
});
// Raise the volume
$('#vUp').click(function() {	
	var volume = $("#jquery_jplayer_1").data("jPlayer").status.volume 
	volume = volume + .1
    $("#jquery_jplayer_1").jPlayer("volume", volume); // 0.0 - 1.0
    $("#volumePercent").html(newValue);
});



}); // End doc

