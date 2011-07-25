$('#mutebutton').click(function() {
    if($('video').prop('muted') == true){
		$('video').prop('muted', false);
		}
	else{
	$('video').prop('muted', true);
	}
});
