/* ------------------------------------------------------------------------
	Class: prettyPhoto
	Use: Lightbox clone for jQuery
	Author: Stephane Caron (http://www.no-margin-for-errors.com)
	Version: 3.1.2
------------------------------------------------------------------------- */

(function($) {
	
	$.prettyPhoto = {version: '3.1.2'};
	
	$.fn.prettyPhoto = function(pp_settings) {
		
		pp_settings = jQuery.extend({
			
			animationSpeed: 'fast', /* fast/slow/normal */
			slideshow: 5000, /* false OR interval time in ms */
			autoplay_slideshow: false, /* true/false */
			opacity: 0.80, /* Value between 0 and 1 */
			showTitle: true, /* true/false */
			allowResize: true, /* Resize the photos bigger than viewport. true/false */
			defaultWidth: 640,
			defaultHeight: 380,
			counter_separator_label: '/', /* The separator for the gallery counter 1 "of" 2 */
			theme: 'pp_default', /* light_rounded / dark_rounded / light_square / dark_square / facebook */
			horizontal_padding: 20, /* The padding on each side of the picture */
			hideflash: false, /* Hides all the flash object on a page, set to TRUE if flash appears over prettyPhoto */
			wmode: 'window', /* Set the flash wmode attribute */
			autoplay: true, /* Automatically start videos: True/False */
			modal: false, /* If set to true, only the close button will close the window */
			deeplinking: true, /* Allow prettyPhoto to update the url to enable deeplinking. */
			showSmallThumbs: true, /* If set to true, a gallery will overlay the fullscreen image on mouse over */
			keyboardShortcuts: true, /* Set to false if you open forms inside prettyPhoto */
			changepicturecallback: function(){}, /* Called everytime an item is shown/changed */
			callback: function(){}, /* Called when prettyPhoto is closed */
			ie6_fallback: false,
			slideshow: false,
			
			markup: '<div class="pp_pic_holder"> \
						<div class="pp_top"> \
							<div class="pp_left"></div> \
							<div class="pp_middle"></div> \
							<div class="pp_right"></div> \
						</div> \
						<div class="pp_content_container"> \
							<div class="pp_left"> \
							<div class="pp_right"> \
								<div class="pp_content"> \
									<div class="pp_loaderIcon"></div> \
									<div class="pp_fade"> \
										<a href="#" class="pp_expand" title="Expand the image">Expand</a> \
										<div class="pp_hoverContainer"> \
											<a class="pp_next" href="#">next</a> \
											<a class="pp_previous" href="#">previous</a> \
										</div> \
										<div id="pp_full_res"></div> \
										<div class="pp_details"> \
											<div class="pp_nav"> \
												<a href="#" class="pp_arrow_previous">Previous</a> \
												<a href="#" class="pp_arrow_next">Next</a> \
											</div> \
											{pp_social} \
											<div class="text-holder"> \
												<p class="currentTextHolder">0/0</p> \
												<p class="pp_description"></p> \
											</div> \
											<a class="pp_close" href="#">Close</a> \
										</div> \
									</div> \
								</div> \
							</div> \
							</div> \
						</div> \
						<div class="pp_bottom"> \
							<div class="pp_left"></div> \
							<div class="pp_middle"></div> \
							<div class="pp_right"></div> \
						</div> \
					</div> \
					<div class="pp_overlay"></div>',
			
			gallery_markup: '<div class="pp_gallery"> \
								<a href="#" class="pp_arrow_previous">Previous</a> \
								<div> \
									<ul> \
										{gallery} \
									</ul> \
								</div> \
								<a href="#" class="pp_arrow_next">Next</a> \
							</div>',
			
			image_markup: '<img id="fullResImage" src="{path}" />',
			
			flash_markup: '<object classid="clsid:D27CDB6E-AE6D-11cf-96B8-444553540000" width="{width}" height="{height}"><param name="wmode" value="{wmode}" /><param name="allowfullscreen" value="true" /><param name="allowscriptaccess" value="always" /><param name="movie" value="{path}" /><embed src="{path}" type="application/x-shockwave-flash" allowfullscreen="true" allowscriptaccess="always" width="{width}" height="{height}" wmode="{wmode}"></embed></object>',
			
			quicktime_markup: '<object classid="clsid:02BF25D5-8C17-4B23-BC80-D3488ABDDC6B" codebase="http://www.apple.com/qtactivex/qtplugin.cab" height="{height}" width="{width}"><param name="src" value="{path}"><param name="autoplay" value="{autoplay}"><param name="type" value="video/quicktime"><embed src="{path}" height="{height}" width="{width}" autoplay="{autoplay}" type="video/quicktime" pluginspage="http://www.apple.com/quicktime/download/"></embed></object>',
			
			iframe_markup: '<iframe id="theFrame" src ="{path}" width="{width}" height="{height}" frameborder="no"></iframe>',
			
			inline_markup: '<div class="pp_inline">{content}</div>',
			
			custom_markup: '<video controls="controls" width="{width}" height="{height}" preload="auto" autoplay="autoplay" id="html5video"><source src="{mp4}" type="video/mp4" /><source src="{webm}" type="video/webm" /><source src="{ogg}" type="video/ogg" />' + 
				
				'<object type="application/x-shockwave-flash" data="{fallback}" width="{width}" height="{height}">' + 
                    
                    '<param name="movie" value="{fallback}" />' + 
                    '<param name="allowScriptAccess" value="sameDomain" />' + 
					'<param name="allowFullScreen" value="true" />' + 
                    '<param name="bgcolor" value="#000000" />' + 
					'<param name="scale" value="noscale" />' +
					'<param name="wmode" value="window" />' +  
					'<param name="quality" value="high" />' + 
					'<param name="salign" value="tl" />' + 
					'<param name="flashvars" value="url={mp4}&wide={width}&tall={height}">' + 

                '</object></video>',
			
			socialTools: '<div class="pp_social"><div class="facebook"><iframe src="http://www.facebook.com/plugins/like.php?locale=en_US&href='+location.href+'&amp;layout=button_count&amp;show_faces=true&amp;width=500&amp;action=like&amp;font&amp;colorscheme=light&amp;height=23" scrolling="no" frameborder="0" style="border:none; overflow:hidden; width:500px; height:23px;" allowTransparency="true"></iframe></div><div class="twitter"><a href="http://twitter.com/share" class="twitter-share-button" data-count="none">Tweet</a><script type="text/javascript" src="http://platform.twitter.com/widgets.js"></script></div><div class="plus_one"><script type="text/javascript" src="https://apis.google.com/js/plusone.js"></script><g:plusone size="medium" count="false"></g:plusone></div></div>'
		
		}, pp_settings);
		
		if(!pp_settings.showShareButtons) pp_settings.socialTools = false;
		
		// Global variables accessible only by prettyPhoto
		var matchedObjects = this, percentBased = false, pp_dimensions, pp_open,
		
		// prettyPhoto container specific
		pp_contentHeight, pp_contentWidth, pp_containerHeight, pp_containerWidth,
		
		// Window size
		windowHeight = $(window).height(), windowWidth = $(window).width(),

		// Global elements
		pp_slideshow,
		
		doresize = true, scroll_pos = _get_scroll();
	
		// Window/Keyboard events
		$(window).unbind('resize.prettyphoto').bind('resize.prettyphoto',function(){ _center_overlay(); _resize_overlay(); });
		
		if(pp_settings.keyboardShortcuts) {
			$(document).unbind('keydown.prettyphoto').bind('keydown.prettyphoto',function(e){
				if(typeof $pp_pic_holder != 'undefined'){
					if($pp_pic_holder.is(':visible')){
						switch(e.keyCode){
							case 37:
								$.prettyPhoto.changePage('previous');
								e.preventDefault();
								break;
							case 39:
								$.prettyPhoto.changePage('next');
								e.preventDefault();
								break;
							case 27:
								if(!settings.modal)
								$.prettyPhoto.close();
								e.preventDefault();
								break;
						};
						// return false;
					};
				};
			});
		};
		
		/**
		* Initialize prettyPhoto.
		*/
		$.prettyPhoto.initialize = function() {
			
			settings = pp_settings;
			makeOnce = true;
			runThisOnce = true;
			firstRun = true;
			dist = null;
			
			isIE7 = (navigator.appVersion.indexOf("MSIE 7.") === -1) ? false : true;
			
			settings.horizontal_padding = 16;
			
			// Find out if the picture is part of a set
			theRel = $(this).attr('rel');
			galleryRegExp = /\[(?:.*)\]/;
			isSet = (galleryRegExp.exec(theRel)) ? true : false;
			
			// Put the SRCs, TITLEs, ALTs into an array.
			pp_images = (isSet) ? jQuery.map(matchedObjects, function(n, i){ if($(n).attr('rel').indexOf(theRel) != -1) return $(n).attr('href'); }) : $.makeArray($(this).attr('href'));
			pp_thumbs = (isSet) ? jQuery.map(matchedObjects, function(n, i){ if($(n).attr('rel').indexOf(theRel) != -1) return $(n).find(".thumb").attr('src'); }) : $.makeArray($(this).find(".thumb").attr('src'));
			
			pp_titles = (isSet) ? jQuery.map(matchedObjects, function(n, i){ if($(n).attr('rel').indexOf(theRel) != -1) return ($(n).find('img').attr('alt')) ? $(n).find('img').attr('alt') : ""; }) : $.makeArray($(this).find('img').attr('alt'));
			pp_descriptions = (isSet) ? jQuery.map(matchedObjects, function(n, i){ if($(n).attr('rel').indexOf(theRel) != -1) return ($(n).attr('title')) ? $(n).attr('title') : ""; }) : $.makeArray($(this).attr('title'));
			
			wasOn = jQuery.inArray($(this).attr('href'), pp_images); // Define where in the array the clicked item is positionned
			set_position = wasOn;
			
			rel_index = (isSet) ? set_position : $("a[rel^='"+theRel+"']").index($(this));
			
			_build_overlay(this); // Build the overlay {this} being the caller
			
			if(settings.allowResize) {
			
				$(window).bind('scroll.prettyphoto',function(){ _center_overlay(); });
				
			}
			
			$.prettyPhoto.open();
			
			return false;
		}

		function checkVid() {
		
			var findVid = $("#html5video");
			
			if(findVid.length) {
				
				try {
					document.getElementById("html5video").pause();
				}
				catch(e) {};
				
				findVid.attr("src", "");
				findVid.empty().remove();
				
			}
			
			findVid = $("#theFrame");
			
			if(findVid.length) findVid.attr("src", "");
			
		}
		
		/**
		* Opens the prettyPhoto modal box.
		* @param image {String,Array} Full path to the image to be open, can also be an array containing full images paths.
		* @param title {String,Array} The title to be displayed with the picture, can also be an array containing all the titles.
		* @param description {String,Array} The description to be displayed with the picture, can also be an array containing all the descriptions.
		*/
		$.prettyPhoto.open = function(event) {
			
			if(typeof settings == "undefined"){ // Means it's an API call, need to manually get the settings and set the variables
				settings = pp_settings;
				//if($.browser.msie && $.browser.version == 6) settings.theme = "light_square"; // Fallback to a supported theme for IE6
				pp_images = $.makeArray(arguments[0]);
				pp_titles = (arguments[1]) ? $.makeArray(arguments[1]) : $.makeArray("");
				pp_descriptions = (arguments[2]) ? $.makeArray(arguments[2]) : $.makeArray("");
				isSet = (pp_images.length > 1) ? true : false;
				wasOn = 0;
				set_position = 0;
				_build_overlay(event.target); // Build the overlay {this} being the caller
			}
			
			checkVid();

			//if($.browser.msie && $.browser.version == 6) $('select').css('visibility','hidden'); // To fix the bug with IE select boxes
			//if(settings.hideflash) $('object,embed,iframe[src*=youtube],iframe[src*=vimeo]').css('visibility','hidden'); // Hide the flash

			_checkPosition($(pp_images).size()); // Hide the next/previous links if on first or last images.
		
			$('.pp_loaderIcon').show();
			$pp_pic_holder.find('.text-holder').css("opacity", 0);
		
			// Fade the content in
			//if($ppt.is(':hidden')) $ppt.css('opacity',0).show();
			$pp_overlay.show().fadeTo(settings.animationSpeed,settings.opacity);
			
			// Display the current position
			if(pp_images.length > 1) {
				$pp_pic_holder.find('.currentTextHolder').text((set_position+1) + settings.counter_separator_label + $(pp_images).size());
				 dash = " - ";
			}
			else {
				$pp_pic_holder.find('.currentTextHolder').hide();
				dash = "";
			}

			// Set the description
			if(pp_descriptions[set_position] != ""){
				$pp_pic_holder.find('.pp_description').show().html(dash + unescape(pp_descriptions[set_position]));
			}else{
				$pp_pic_holder.find('.pp_description').hide();
			}
			
			// Get the dimensions
			movie_width = ( parseFloat(getParam('width',pp_images[set_position])) ) ? getParam('width',pp_images[set_position]) : settings.defaultWidth.toString();
			movie_height = ( parseFloat(getParam('height',pp_images[set_position])) ) ? getParam('height',pp_images[set_position]) : settings.defaultHeight.toString();
			
			// If the size is % based, calculate according to window dimensions
			percentBased=false;
			if(movie_height.indexOf('%') != -1) { movie_height = parseFloat(($(window).height() * parseFloat(movie_height) / 100) - 150); percentBased = true; }
			if(movie_width.indexOf('%') != -1) { movie_width = parseFloat(($(window).width() * parseFloat(movie_width) / 100) - 150); percentBased = true; }
			
			// Fade the holder
			$pp_pic_holder.fadeIn(function(){
				// Set the title
				//(settings.showTitle && pp_titles[set_position] != "" && typeof pp_titles[set_position] != "undefined") ? $ppt.html(unescape(pp_titles[set_position])) : $ppt.html('&nbsp;');
				
				imgPreloader = "";
				skipInjection = false;
				
				// Inject the proper content
				switch(_getFileType(pp_images[set_position])){
					case 'image':
						imgPreloader = new Image();

						// Preload the neighbour images
						nextImage = new Image();
						if(isSet && set_position < $(pp_images).size() -1) nextImage.src = pp_images[set_position + 1];
						prevImage = new Image();
						if(isSet && pp_images[set_position - 1]) prevImage.src = pp_images[set_position - 1];

						$pp_pic_holder.find('#pp_full_res')[0].innerHTML = settings.image_markup.replace(/{path}/g,pp_images[set_position]);

						imgPreloader.onload = function(){
							// Fit item to viewport
							pp_dimensions = _fitToViewport(imgPreloader.width,imgPreloader.height);

							_showContent();
						};

						imgPreloader.onerror = function(){
							alert('Image cannot be loaded. Make sure the path is correct and image exist.');
							$.prettyPhoto.close();
						};
					
						imgPreloader.src = pp_images[set_position];
					break;
				
					case 'youtube':
						pp_dimensions = _fitToViewport(movie_width,movie_height); // Fit item to viewport

						movie = 'http://www.youtube.com/embed/'+getParam('v',pp_images[set_position]);
						(getParam('rel',pp_images[set_position])) ? movie+="?rel="+getParam('rel',pp_images[set_position]) : movie+="?rel=1";
						
						movie += "&autohide=1&hd=1&iv_load_policy=3&showinfo=0&showsearch=0";	
						if(settings.autoplay) movie += "&autoplay=1";
					
						toInject = settings.iframe_markup.replace(/{width}/g,pp_dimensions['width']).replace(/{height}/g,pp_dimensions['height']).replace(/{wmode}/g,settings.wmode).replace(/{path}/g,movie);
					break;
				
					case 'vimeo':
						pp_dimensions = _fitToViewport(movie_width,movie_height); // Fit item to viewport
					
						movie_id = pp_images[set_position];
						var regExp = /http:\/\/(www\.)?vimeo.com\/(\d+)/;
						var match = movie_id.match(regExp);
						
						movie = 'http://player.vimeo.com/video/'+ match[2] +'?title=0&amp;byline=0&amp;portrait=0';
						movie += "&amp;color=" + settings.vimeoSkinColor.split("#").join("");
						if(settings.autoplay) movie += "&amp;autoplay=1;";
				
						vimeo_width = pp_dimensions['width'] + '/embed/?moog_width='+ pp_dimensions['width'];
				
						toInject = settings.iframe_markup.replace(/{width}/g,vimeo_width).replace(/{height}/g,pp_dimensions['height']).replace(/{path}/g,movie);
					break;
				
					case 'quicktime':
						pp_dimensions = _fitToViewport(movie_width,movie_height); // Fit item to viewport
						pp_dimensions['height']+=15; pp_dimensions['contentHeight']+=15; pp_dimensions['containerHeight']+=15; // Add space for the control bar
				
						toInject = settings.quicktime_markup.replace(/{width}/g,pp_dimensions['width']).replace(/{height}/g,pp_dimensions['height']).replace(/{wmode}/g,settings.wmode).replace(/{path}/g,pp_images[set_position]).replace(/{autoplay}/g,settings.autoplay);
					break;
				
					case 'flash':
						pp_dimensions = _fitToViewport(movie_width,movie_height); // Fit item to viewport
					
						flash_vars = pp_images[set_position];
						flash_vars = flash_vars.substring(pp_images[set_position].indexOf('flashvars') + 10,pp_images[set_position].length);

						filename = pp_images[set_position];
						filename = filename.substring(0,filename.indexOf('?'));
					
						toInject =  settings.flash_markup.replace(/{width}/g,pp_dimensions['width']).replace(/{height}/g,pp_dimensions['height']).replace(/{wmode}/g,settings.wmode).replace(/{path}/g,filename+'?'+flash_vars);
					break;
				
					case 'iframe':
						pp_dimensions = _fitToViewport(movie_width,movie_height); // Fit item to viewport
				
						frame_url = pp_images[set_position];
						frame_url = frame_url.substr(0,frame_url.indexOf('iframe')-1);

						toInject = settings.iframe_markup.replace(/{width}/g,pp_dimensions['width']).replace(/{height}/g,pp_dimensions['height']).replace(/{path}/g,frame_url);
					break;
					
					case 'ajax':
						doresize = false; // Make sure the dimensions are not resized.
						pp_dimensions = _fitToViewport(movie_width,movie_height);
						doresize = true; // Reset the dimensions
					
						skipInjection = true;
						$.get(pp_images[set_position],function(responseHTML){
							toInject = settings.inline_markup.replace(/{content}/g,responseHTML);
							$pp_pic_holder.find('#pp_full_res')[0].innerHTML = toInject;
							_showContent();
						});
						
					break;
					
					case 'custom':
					
						pp_dimensions = _fitToViewport(movie_width, movie_height); // Fit item to viewport
						filename = pp_images[set_position];
						filename = filename.substring(0,filename.indexOf('?'));
						toInject = settings.custom_markup.replace(/{width}/g, pp_dimensions['width']).replace(/{height}/g, pp_dimensions['height']).replace(/{mp4}/g, filename).replace(/{webm}/g, filename.replace("mp4", "webm")).replace(/{ogg}/g, filename.replace("mp4", "ogv")).replace(/{fallback}/g, settings.flashVideoSwf);
						
					break;
				
					case 'inline':
						// to get the item height clone it, apply default width, wrap it in the prettyPhoto containers , then delete
						myClone = $(pp_images[set_position]).clone().append('<br clear="all" />').css({'width':settings.defaultWidth}).wrapInner('<div id="pp_full_res"><div class="pp_inline"></div></div>').appendTo($('body')).show();
						doresize = false; // Make sure the dimensions are not resized.
						pp_dimensions = _fitToViewport($(myClone).width(),$(myClone).height());
						doresize = true; // Reset the dimensions
						$(myClone).remove();
						toInject = settings.inline_markup.replace(/{content}/g,$(pp_images[set_position]).html());
					break;
				};

				if(!imgPreloader && !skipInjection){
					$pp_pic_holder.find('#pp_full_res')[0].innerHTML = toInject;
				
					// Show content
					_showContent();
				};
			});
			
			return false;
		};

	
		/**
		* Change page in the prettyPhoto modal box
		* @param direction {String} Direction of the paging, previous or next.
		*/
		$.prettyPhoto.changePage = function(direction){
			
			wasOn = set_position;
			
			if(direction == 'previous') {
				set_position--;
				if (set_position < 0) set_position = $(pp_images).size()-1;
			}else if(direction == 'next'){
				set_position++;
				if(set_position > $(pp_images).size()-1) set_position = 0;
			}else{
				set_position=direction;
			};
			
			rel_index = set_position;

			if(!doresize) doresize = true; // Allow the resizing of the images
			//$('.pp_contract').removeClass('pp_contract').addClass('pp_expand');

			_hideContent(function(){ $.prettyPhoto.open(); });
			
		};

		/**
		* Change gallery page in the prettyPhoto modal box
		* @param direction {String} Direction of the paging, previous or next.
		*/
		$.prettyPhoto.changeGalleryPage = function(direction){

			if(direction == "next"){
				
				if(currentGalleryPage < pp_images.length - itemsPerPage) {
					
					currentGalleryPage++;
					
				}
				else {
					
					return;
				
				}
				
			}

			else if(direction == "previous"){

				if(currentGalleryPage > 0) {
					
					currentGalleryPage--;
					
				}
				else {
				
					return;
					
				}
				
			}
			else if(firstRun) {
				
				firstRun = false;
				
				if(direction > pp_images.length - itemsPerPage) {
						
					currentGalleryPage = pp_images.length - itemsPerPage;
							
				}
				else {
				
					currentGalleryPage = direction;
					
				}
				
			}
			else {
				
				if(direction == 0 && wasOn == pp_images.length - 1) {
					
					currentGalleryPage = 0;
					
				}
				else if(direction == pp_images.length - 1 && wasOn == 0) {
					
					currentGalleryPage = pp_images.length - itemsPerPage;
					
				}
				else {
					
					var changedUp = false, changedDown = false;
					
					if(direction > currentGalleryPage) {
						
						if(currentGalleryPage + itemsPerPage - 1 < direction) {
							
							currentGalleryPage++;
							changedUp = true;
							
						}
						
					}
					else if(direction < currentGalleryPage) {
						
						if(currentGalleryPage + itemsPerPage - 1 > direction) {
						
							currentGalleryPage--;
							changedDown = true;
							
						}
						
					}
					else {
					
						currentGalleryPage = direction;
						
					}
					
					if(changedUp || changedDown) {
						
						if(direction < currentGalleryPage + itemsPerPage - 1 || direction > currentGalleryPage + itemsPerPage - 1) {
							
							if(currentGalleryPage + itemsPerPage > pp_images.length - itemsPerPage) {
								
								if(changedUp) {
								
									currentGalleryPage = direction;
									
									if(currentGalleryPage + itemsPerPage > pp_images.length - itemsPerPage) {
										
										currentGalleryPage = pp_images.length - itemsPerPage;
										
									}
									
								}
								else {
								
									currentGalleryPage = direction;
									
								}		
							}	
						}	
					}	
				}
			}
			
			toMove = -(currentGalleryPage * 82);
			
			if(dist !== toMove) {
			
				$pp_gallery.find('ul').animate({left: toMove}, 200);
				
			}
			
			dist = toMove;
			
		};


		/**
		* Start the slideshow...
		*/
		$.prettyPhoto.startSlideshow = function(){
			if(typeof pp_slideshow == 'undefined'){
				$pp_pic_holder.find('.pp_play').unbind('click').removeClass('pp_play').addClass('pp_pause').click(function(){
					$.prettyPhoto.stopSlideshow();
					return false;
				});
				pp_slideshow = setInterval($.prettyPhoto.startSlideshow,settings.slideshow);
			}else{
				$.prettyPhoto.changePage('next');	
			};
		}


		/**
		* Stop the slideshow...
		*/
		$.prettyPhoto.stopSlideshow = function(){
			$pp_pic_holder.find('.pp_pause').unbind('click').removeClass('pp_pause').addClass('pp_play').click(function(){
				$.prettyPhoto.startSlideshow();
				return false;
			});
			clearInterval(pp_slideshow);
			pp_slideshow=undefined;
		}


		/**
		* Closes prettyPhoto.
		*/
		$.prettyPhoto.close = function(){
			
			if($pp_overlay.is(":animated")) return;
			
			checkVid();
			
			$.prettyPhoto.stopSlideshow();
			
			$pp_pic_holder.stop().find('object,embed').css('visibility','hidden');
			
			$('div.pp_pic_holder,.pp_fade').fadeOut(settings.animationSpeed,function(){ $(this).remove(); });
			
			$pp_overlay.fadeOut(settings.animationSpeed, function(){
				
				//if($.browser.msie && $.browser.version == 6) $('select').css('visibility','visible'); // To fix the bug with IE select boxes
				//if(settings.hideflash) $('object,embed,iframe[src*=youtube],iframe[src*=vimeo]').css('visibility','visible'); // Show the flash
				
				$(this).remove(); // No more need for the prettyPhoto markup
				
				$(window).unbind('scroll.prettyphoto');
				
				settings.callback();
				
				doresize = true;
				
				pp_open = false;
				
				checkVid();
				
				delete settings;
			});
			
		};
	
		/**
		* Set the proper sizes on the containers and animate the content in.
		*/
		function _showContent(){
			
			$('.pp_loaderIcon').hide();

			// Calculate the opened top position of the pic holder
			projectedTop = scroll_pos['scrollTop'] + ((windowHeight/2) - (pp_dimensions['containerHeight']/2));
			if(projectedTop < 0) projectedTop = 0;

			//$ppt.fadeTo(settings.animationSpeed, 1, function() {setTimeout(fixText, 50);});

			// Resize the content holder
			$pp_pic_holder.find('.pp_content')
				.animate({
					height:pp_dimensions['contentHeight'],
					width:pp_dimensions['contentWidth']
				},settings.animationSpeed);
			
			// Resize picture the holder
			$pp_pic_holder.animate({
				'top': projectedTop,
				'left': (windowWidth/2) - (pp_dimensions['containerWidth']/2),
				width:pp_dimensions['containerWidth']
			},settings.animationSpeed,function(){
				$pp_pic_holder.find('.pp_hoverContainer,#fullResImage').height(pp_dimensions['height']).width(pp_dimensions['width']);

				$pp_pic_holder.find('.pp_fade').fadeIn(settings.animationSpeed); // Fade the new content

				// Show the nav
				if(isSet && _getFileType(pp_images[set_position])=="image") { 

					$pp_pic_holder.find('.pp_hoverContainer').css("visibility", "visible");
					
				}
				else{ 
				
					$pp_pic_holder.find('.pp_hoverContainer').css("visibility", "hidden");
					
				}
				
				/*
				if(pp_dimensions['resized']){ // Fade the resizing link if the image is resized
					$('a.pp_expand,a.pp_contract').show();
				}else{
					$('a.pp_expand').hide();
				}
				*/
				
				if(settings.autoplay_slideshow && !pp_slideshow && !pp_open) $.prettyPhoto.startSlideshow();
				
				if(settings.deeplinking)
					setHashtag();
				
				settings.changepicturecallback(); // Callback!
				
				pp_open = true;
				
				setTimeout(fixText, 50);
				
			});
			
			var pg = $pp_pic_holder.find('.pp_content');
			
			if(_getFileType(pp_images[set_position])=="image") { 
				
				pg.hover(
					function(){
						$pp_pic_holder.find('.pp_gallery').stop(true, true).css({display: "none", visibility: "visible"}).fadeIn();
					},
					function(){
						$pp_pic_holder.find('.pp_gallery').stop(true, true).css({display: "block", visibility: "visible"}).fadeOut();
					});
				
				if(pg.data("isHidden")) {
					
					$pp_pic_holder.find('.pp_gallery').stop(true, true).fadeIn();
					pg.data("isHidden", false);
					
				}
				
				_insert_gallery();
					
			}
			else{ 
				
				pg.unbind('mouseenter mouseleave').data("isHidden", true);
				$pp_pic_holder.find('.pp_gallery').hide();
					
			}
				
			
		};
		
		function fixText() {
		
			$pp_pic_holder.find(".text-holder").css("margin-left", -(Math.round(($pp_pic_holder.find(".pp_description").width() + $pp_pic_holder.find(".currentTextHolder").width()) * 0.5)) - 2).animate({opacity: 1}, "fast");
			
		}
		
		/**
		* Hide the content...DUH!
		*/
		function _hideContent(callback){
			
			$pp_gallery.find('ul').stop(true, true);
			
			// Fade out the current picture
			$pp_pic_holder.find('#pp_full_res object,#pp_full_res embed').css('visibility','hidden');
			$pp_pic_holder.find('.pp_fade').fadeOut(settings.animationSpeed,function(){
				$('.pp_loaderIcon').show();
				
				callback();
			});
		};
	
		/**
		* Check the item position in the gallery array, hide or show the navigation links
		* @param setCount {integer} The total number of items in the set
		*/
		function _checkPosition(setCount){
			(setCount > 1) ? $('.pp_nav').show() : $('.pp_nav').hide(); // Hide the bottom nav if it's not a set.
		};
	
		/**
		* Resize the item dimensions if it's bigger than the viewport
		* @param width {integer} Width of the item to be opened
		* @param height {integer} Height of the item to be opened
		* @return An array containin the "fitted" dimensions
		*/
		function _fitToViewport(width,height){
			resized = false;

			_getDimensions(width,height);
			
			// Define them in case there's no resize needed
			imageWidth = width, imageHeight = height;

			if( ((pp_containerWidth > windowWidth) || (pp_containerHeight > windowHeight)) && doresize && settings.allowResize && !percentBased) {
				resized = true, fitting = false;
			
				while (!fitting){
					if((pp_containerWidth > windowWidth)){
						imageWidth = (windowWidth - 200);
						imageHeight = (height/width) * imageWidth;
					}else if((pp_containerHeight > windowHeight)){
						imageHeight = (windowHeight - 200);
						imageWidth = (width/height) * imageHeight;
					}else{
						fitting = true;
					};

					pp_containerHeight = imageHeight, pp_containerWidth = imageWidth;
				};
			
				_getDimensions(imageWidth,imageHeight);
				
				if((pp_containerWidth > windowWidth) || (pp_containerHeight > windowHeight)){
					_fitToViewport(pp_containerWidth,pp_containerHeight)
				};
			};
			
			return {
				width:Math.floor(imageWidth),
				height:Math.floor(imageHeight),
				containerHeight:Math.floor(pp_containerHeight),
				containerWidth:Math.floor(pp_containerWidth) + (settings.horizontal_padding * 2),
				contentHeight:Math.floor(pp_contentHeight),
				contentWidth:Math.floor(pp_contentWidth),
				resized:resized
			};
		};
		
		/**
		* Get the containers dimensions according to the item size
		* @param width {integer} Width of the item to be opened
		* @param height {integer} Height of the item to be opened
		*/
		function _getDimensions(width,height){
			width = parseFloat(width);
			height = parseFloat(height);
			
			// Get the details height, to do so, I need to clone it since it's invisible
			$pp_details = $pp_pic_holder.find('.pp_details');
			$pp_details.width(width);
			var detailsHeight = parseFloat($pp_details.css('marginTop')) + parseFloat($pp_details.css('marginBottom'));
			
			$pp_details = $pp_details.clone().addClass(settings.theme).width(width).appendTo($('body')).css({
				'position':'absolute',
				'top':-10000
			});
			detailsHeight += $pp_details.height();
			detailsHeight = 28; // Min-height for the details
			//if($.browser.msie && $.browser.version==7) detailsHeight+=8;
			$pp_details.remove();
			
			// Get the titles height, to do so, I need to clone it since it's invisible
			//$pp_title = $pp_pic_holder.find('.ppt');
			//$pp_title.width(width);
			//titleHeight = parseFloat($pp_title.css('marginTop')) + parseFloat($pp_title.css('marginBottom'));
			
			/*
			$pp_title = $pp_title.clone().appendTo($('body')).css({
				'position':'absolute',
				'top':-10000
			});
			titleHeight += $pp_title.height();
			$pp_title.remove();
			*/
			
			// Get the container size, to resize the holder to the right dimensions
			pp_contentHeight = height + detailsHeight;
			pp_contentWidth = width;
			pp_containerHeight = pp_contentHeight + $pp_pic_holder.find('.pp_top').height() + $pp_pic_holder.find('.pp_bottom').height();
			pp_containerWidth = width;
			
		}
	
		function _getFileType(itemSrc){
			if (itemSrc.match(/youtube\.com\/watch/i)) {
				return 'youtube';
			}else if (itemSrc.match(/vimeo\.com/i)) {
				return 'vimeo';
			}else if(itemSrc.match(/\b.mov\b/i)){ 
				return 'quicktime';
			}else if(itemSrc.match(/\b.swf\b/i)){
				return 'flash';
			}else if(itemSrc.match(/\biframe=true\b/i)){
				return 'iframe';
			}else if(itemSrc.match(/\bajax=true\b/i)){
				return 'ajax';
			}else if(itemSrc.match(/\bcustom=true\b/i)){
				return 'custom';
			}else if(itemSrc.substr(0,1) == '#'){
				return 'inline';
			}else{
				return 'image';
			};
		};
	
		function _center_overlay(){
			if(doresize && typeof $pp_pic_holder != 'undefined') {
				
				scroll_pos = _get_scroll();
				contentHeight = $pp_pic_holder.height(), contentwidth = $pp_pic_holder.width();

				projectedTop = (windowHeight/2) + scroll_pos['scrollTop'] - (contentHeight/2);
				if(projectedTop < 0) projectedTop = 0;
				
				if(contentHeight > windowHeight)
					return;

				$pp_pic_holder.css({
					'top': projectedTop,
					'left': (windowWidth/2) + scroll_pos['scrollLeft'] - (contentwidth/2)
				});
			};
		};
	
		function _get_scroll(){
			if (self.pageYOffset) {
				return {scrollTop:self.pageYOffset,scrollLeft:self.pageXOffset};
			} else if (document.documentElement && document.documentElement.scrollTop) { // Explorer 6 Strict
				return {scrollTop:document.documentElement.scrollTop,scrollLeft:document.documentElement.scrollLeft};
			} else if (document.body) {// all other Explorers
				return {scrollTop:document.body.scrollTop,scrollLeft:document.body.scrollLeft};
			};
		};
	
		function _resize_overlay() {
			
			windowHeight = $(window).height(), windowWidth = $(window).width();
			
			if(typeof $pp_overlay != "undefined") $pp_overlay.height($(document).height()).width(windowWidth);
			
		};
	
		function _insert_gallery(){
			
			if(makeOnce) {
				
				makeOnce = false;
				
				if(isSet && settings.showSmallThumbs) {
					
					var galleryWidth, navWidth = 50, itemWidth = 82; // 52 beign the thumb width, 5 being the right margin.
					
					itemsPerPage = settings.maxVisibleSmallThumbs;
					if(pp_images.length < itemsPerPage) itemsPerPage = pp_images.length;
	
					// Hide the nav in the case there's no need for links
					if(Math.ceil(pp_images.length / itemsPerPage) - 1 == 0){
						navWidth = 0; // No nav means no width!
						$pp_gallery.find('.pp_arrow_next,.pp_arrow_previous').hide();
					}
					else {
						$pp_gallery.find('.pp_arrow_next,.pp_arrow_previous').show();
					};
	
					galleryWidth = itemsPerPage * itemWidth;
					
					// Set the proper width to the gallery items
					$pp_gallery
						.css('margin-left',-((galleryWidth/2) + (navWidth/2)) - 5)
						.find('div:first').width(galleryWidth + 5)
						.find('ul').width(pp_images.length * itemWidth);
					
					hasGallery = true;
					
				}
				
				else {
					
					$pp_pic_holder.find('.pp_content').data("isHidden", true).unbind('mouseenter mouseleave').hide();
					hasGallery = false;
					return;
					
					// $pp_gallery.hide();
					
				}
				
				if(navigator.userAgent.search("iPhone") === -1 && navigator.userAgent.search("iPod") === -1) {}
				
				else {
				
					hasGallery = false;
					$pp_gallery.empty();
					
				}
				
			}
			
			if(hasGallery) {
				
				// Set the proper width to the gallery items
				$pp_gallery.find('li.selected').removeClass('selected');	
				$pp_gallery_li.filter(':eq('+set_position+')').addClass('selected');
					
				$.prettyPhoto.changeGalleryPage(set_position);
				
			}
			
		}
	
		function _build_overlay(caller){
			
			if(pp_callerBuilt) {
				
				settings.socialTools.split('<script type="text/javascript" src="http://platform.twitter.com/widgets.js"></script>').join("");
				settings.socialTools.split('<script type="text/javascript" src="https://apis.google.com/js/plusone.js"></script>').join("");
					
			}
			
			pp_callerBuilt = true;
				
			settings.markup=settings.markup.replace('{pp_social}',(settings.socialTools)?settings.socialTools:'');
			
			$('body').append(settings.markup); // Inject the markup
			
			$pp_pic_holder = $('.pp_pic_holder') , $pp_overlay = $('div.pp_overlay'); // Set my global selectors
			
			// Inject the inline gallery!
			if(isSet && settings.showSmallThumbs) {
				
				currentGalleryPage = 0;
				
				toInject = "";
				for (var i=0; i < pp_images.length; i++) {
					if(!pp_thumbs[i].match(/\b(jpg|jpeg|png|gif)\b/gi)){
						classname = 'default';
						img_src = '';
					}else{
						classname = '';
						img_src = pp_thumbs[i];
					}
					toInject += "<li class='"+classname+"'><a href='#'><img src='" + img_src + "' width='75' alt='' /></a></li>";
				};
				
				toInject = settings.gallery_markup.replace(/{gallery}/g,toInject);
				
				$pp_pic_holder.find('#pp_full_res').after(toInject);
				
				$pp_gallery = $('.pp_pic_holder .pp_gallery'), $pp_gallery_li = $pp_gallery.find('li'); // Set the gallery selectors
				
				$pp_gallery.find('.pp_arrow_next').click(function(){
					$.prettyPhoto.changeGalleryPage('next');
					$.prettyPhoto.stopSlideshow();
					return false;
				});
				
				$pp_gallery.find('.pp_arrow_previous').click(function(){
					$.prettyPhoto.changeGalleryPage('previous');
					$.prettyPhoto.stopSlideshow();
					return false;
				});

				$pp_gallery_li.each(function(i){
					$(this)
						.find('a')
						.click(function(){
							$.prettyPhoto.changePage(i);
							$.prettyPhoto.stopSlideshow();
							return false;
						});
				});
			};
			
			
			// Inject the play/pause if it's a slideshow
			if(settings.slideshow){
				$pp_pic_holder.find('.pp_nav').prepend('<a href="#" class="pp_play">Play</a>')
				$pp_pic_holder.find('.pp_nav .pp_play').click(function(){
					$.prettyPhoto.startSlideshow();
					return false;
				});
			}
			
			$pp_pic_holder.attr('class','pp_pic_holder ' + settings.theme); // Set the proper theme
			
			$pp_overlay
				.css({
					'opacity':0,
					'height':$(document).height(),
					'width':$(window).width()
					})
				.bind('click',function(){
					if(!settings.modal) $.prettyPhoto.close();
				});

			$('a.pp_close').bind('click',function(){ $.prettyPhoto.close(); return false; });
			
			/*
			$('a.pp_expand').bind('click',function(e){
				// Expand the image
				if($(this).hasClass('pp_expand')){
					$(this).removeClass('pp_expand').addClass('pp_contract');
					doresize = false;
				}else{
					$(this).removeClass('pp_contract').addClass('pp_expand');
					doresize = true;
				};
			
				_hideContent(function(){ $.prettyPhoto.open(); });
		
				return false;
			});
			*/
		
			$pp_pic_holder.find('.pp_previous, .pp_nav .pp_arrow_previous').bind('click',function(){
				$.prettyPhoto.changePage('previous');
				$.prettyPhoto.stopSlideshow();
				return false;
			});
		
			$pp_pic_holder.find('.pp_next, .pp_nav .pp_arrow_next').bind('click',function(){
				$.prettyPhoto.changePage('next');
				$.prettyPhoto.stopSlideshow();
				return false;
			});
			
			_center_overlay(); // Center it
		};

		if(!pp_alreadyInitialized && getHashtag()){
			
			pp_alreadyInitialized = true;
			
			// Grab the rel index to trigger the click on the correct element
			var hashIndex = getHashtag(), hashRel = hashIndex;
			
			hashIndex = hashIndex.substring(hashIndex.indexOf('/')+1,hashIndex.length-1);
			hashRel = hashRel.substring(0,hashRel.indexOf('/'));

			// Little timeout to make sure all the prettyPhoto initialize scripts has been run.
			// Useful in the event the page contain several init scripts.
			setTimeout(function(){ $("a[rel^='"+hashRel+"']:eq("+hashIndex+")").trigger('click'); },50);
		}
		
		return this.unbind('click.prettyphoto').bind('click.prettyphoto',$.prettyPhoto.initialize); // Return the jQuery object for chaining. The unbind method is used to avoid click conflict when the plugin is called more than once
	};
	
	function getHashtag(){
		
		var url = location.href;
		
		return (url.indexOf('#!') != -1) ? decodeURI(url.substring(url.indexOf('#!')+2,url.length)) : false;

	};
	
	function setHashtag(){
		if(typeof theRel == 'undefined') return; // theRel is set on normal calls, it's impossible to deeplink using the API
		location.hash = '!' + theRel + '/'+rel_index+'/';
	};
	
	function getParam(name,url){
	  name = name.replace(/[\[]/,"\\\[").replace(/[\]]/,"\\\]");
	  var regexS = "[\\?&]"+name+"=([^&#]*)", regex = new RegExp( regexS ), results = regex.exec( url );
	  return ( results == null ) ? "" : results[1];
	}
	
})(jQuery);

var pp_callerBuilt = false, pp_alreadyInitialized = false; // Used for the deep linking to make sure not to call the same function several times.