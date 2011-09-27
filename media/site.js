$(document).ready(function(){	
		
		$('#guideList').isotope({
		  // options
		  itemSelector : '.guide_thumb',
		  layoutMode : 'fitRows'
		});
		

		$('#filters a').click(function(){
		  var selector = $(this).attr('data-filter');
		  $('#guideList').isotope({ filter: selector });
		  return false;
		});
		
		
});