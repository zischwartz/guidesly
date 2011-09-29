$(document).ready(function(){	
		
		
	//popovers
	$("a[rel=popover]").popover({
	                  offset: 10,
	                  html: true,
					  delayOut: 100,
					  delayIn: 100
	                })
	                .click(function(e) {
	                  e.preventDefault()
	                })
		
		// Topbar Menu
		$("body").bind("click", function (e) {$('a.menu').parent("li").removeClass("open");});
		$("a.menu").click(function (e) {var $li = $(this).parent("li").toggleClass('open'); return false; });
	
	
	
		//check to see if we're on a page with a guidelisting
		// to do isotope pretty filtering and such

		if ($('#guideList').length)
		{
			$('#guideList').isotope({
			  itemSelector : '.guideBox',
			  layoutMode : 'fitRows'
			});
		
			$('#popular_tags a').click(function(){
			  var selector = $(this).attr('data-filter');
			  $('#guideList').isotope({ filter: selector });
			 $("#popular_tags ul li.active").removeClass("active");
			 $(this).parent().addClass("active");
			  return false;
			
			});
			
			
			
		} //end if guidelist exists on the page.
		

		
});