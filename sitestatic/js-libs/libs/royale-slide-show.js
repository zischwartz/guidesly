(function($) {
	
	$.royaleSlideShow = function(sets) {
		
		// RETURN IF SETTINGS ARE UNDEFINED
		if(typeof sets === "undefined") {
		
			alert("slideShowSettings need to be defined");
			return;
			
		}
		
		if($("#top-slideshow").length === 0 || $("#banner-slideshow").length === 0) return false;
		
		// GLOBAL VARS
		var urls = [],
		buttons = [],
		targets = [],
		media = [],
		links = [],
		descs = [],
		
		imgOne,
		imgTwo,
		iCount,
		vButton,
		timeout,
		hasMedia,
		
		isOn = 0,
		wasOn = 0,
		imgOn = 0,
		plusZ = 0,
		counter = 0,
		cover = null,
		running = true,
		firstRun = true,
		readyToFire = true,
		
		useText = sets.useText,
		wide = sets.imageWidth,
		tall = sets.imageHeight,
		wider = wide.toString(),
		taller = tall.toString(),
		autoplay = sets.autoPlay,
		delay = sets.autoPlayDelay,
		vimeoColor,
		flashURL,
		
		top = $("#top-slideshow"),
		banner = $("#banner-slideshow").css("overflow", "hidden"),
		container = $("<div />").css("overflow", "hidden").prependTo(top),
		
		divTwo = $("<div />").css({
			
			position: "absolute", 
			clip: "rect(0px, " + wider + "px, " + taller + "px, 0px)"
			
		}).appendTo(container),
		
		divOne = $("<div />").css({
			
			position: "absolute", 
			clip: "rect(0px, " + wider + "px, " + taller + "px, 0px)", width: wide, height: tall
			
		}).appendTo(container);
		
		vimeoColor = sets.vimeoSkinColor.split("#").join(""),
		flashURL = sets.flashVideoSwf;
		
		if(autoplay) top.mouseenter(enterBanner).mouseleave(exitBanner); 
		
		init(sets);
		
		settings = null;
		container = null;
		
		// INIT FUNCTION
		function init(data) {
			
			var btnHolder = $("<div />").appendTo(top),
			items = $("#banner-slideshow ul li"),
			plus = 0,
			margRight,
			button,
			arLeg,
			st,
			ar,
			i;
			
			// Text
			if(useText) {
				
				if(data.textAlign === "right") {
				
					banner.css("left", wide + sets.textMargin);
					
				}
				else {
					
					plus = parseInt(items.css("width"), 10) + sets.textMargin;
					container.css("margin-left",  plus);
					
				}
				
			}
			
			$("<div />").css({height: tall}).appendTo(banner);
			
			// LOOP THROUGH ALL SLIDES
			items.each(function() {
				
				if(counter === 0) $(this).css({position: "absolute", left: 0});
				
				descs[counter] = $(this);
				links[counter] = 0;
				targets[counter] = 0;
				media[counter] = 0;
				
				$(this).css({paddingLeft: 0, paddingRight: 0});
				
				if(!$(this).attr("title")) {
				
					alert("slideshow media must be defined");
					return false;
					
				}
				
				ar = $(this).attr("title").split("&");
				arLeg = ar.length;
				
				for(i = 0; i < arLeg; i++) {
					
					st = ar[i];
					
					if(st.search("image=") !== -1) urls[counter] = st.substr(6, st.length);
					else if(st.search("link=") !== -1) links[counter] = st.substr(5, st.length);
					else if(st.search("target=") !== -1) targets[counter] = st.substr(7, st.length);
					else if(st.search("media=") !== -1) media[counter] = st.substr(6, st.length);	
					
				}
				
				button = $("<div />").addClass("slide-show-button").data("id", counter).appendTo(btnHolder);
				buttons[counter] = button;
				
				$(this).removeAttr("title");
				counter++;
				
			});
			
			iCount = counter - 1;
			
			// IF SLIDESHOW ITEMS HAD URLS
			if(urls.length) {
				
				button = buttons[0];
				margRight = parseInt(button.css("margin-right"), 10);
				
				btnHolder.css({
					
					position: "absolute",
					top: banner.offset().top + tall,
					left: plus + (Math.round(wide >> 1)) - (((items.length * (parseInt(button.css("width"), 10) + margRight)) - margRight) >> 1) + parseInt(container.css("padding-left"), 10)
					
				});
				
				button.addClass("slide-show-button-active");
				
				imgOne = $("<img />").css({position: "absolute", display: "none"}).load(loaded).appendTo(divOne);
				
				if(links[0] !== 0) imgOne.css("cursor", "pointer").click(gotoURL);
				
				if(media[0] === 0) {
					
					hasMedia = false;
					
				}
				else {
				
					hasMedia = true;
					videoButton(divOne);
					vButton.css("opacity", 0).mouseover(vOver).mouseout(vOut).click(activateVideo);
					
				}
				
				imgOne.attr("src", urls[0]);
				if(useText) descs[0].css("display", "block");
					
			}
			else {
			
				btnHolder.detatch();
				
			}
			
			banner = null;
			top = null;
			
		}
		
		// PAUSE SLIDESHOW ON MOUSE OVER
		function enterBanner(event) {
			
			event.stopPropagation();
			
			if(timeout) clearTimeout(timeout);
			
			readyToFire = false;
			
		}
		
		// UNPAUSE SLIDESHOW ON MOUSEOVER
		function exitBanner(event) {
			
			event.stopPropagation();
			
			readyToFire = true;
			
			if(!running) timeout = setTimeout(nextSlide, delay);
			
		}
		
		// CREATE VIDEO BUTTONS
		function videoButton(theDiv) {
		
			cover = $("<div />").css("position", "absolute").appendTo(theDiv);
			vButton = $("<div />").addClass("play-video-button").appendTo(cover);
					
			vButton.css({
						
				top: Math.round((tall >> 1) - (parseInt(vButton.css("height"), 10) >> 1)), 
				left: Math.round((wide >> 1) - (parseInt(vButton.css("width"), 10) >> 1))
							
			});
			
		}
		
		// VIDEO BUTTON MOUSE OVER
		function vOver() {
		
			vButton.stop(true).animate({"opacity": 1}, 300);
			
		}
		
		// VIDEO BUTTON MOUSE OUT
		function vOut() {
		
			vButton.stop(true).animate({"opacity": 0.7}, 250);
			
		}
		
		// ATTACH VIDEO TO SLIDESHOW
		function activateVideo() {
			
			if(timeout) clearTimeout(timeout);
			
			vButton.unbind("click", activateVideo).unbind("mouseover", vOver).unbind("mouseout", vOut);
			
			// YOUTUBE VIDEO
			if(media[isOn].search("youtube.com") !== -1) {
				
				var st = "http://www.youtube.com/embed/" + media[isOn].split("watch?v=")[1] + "?autoplay=1&autohide=1&hd=1&iv_load_policy=3&showinfo=0&showsearch=0&wmode=transparent";
				
				cover.html('<iframe class="youtube-player" type="text/html" width="' + wide.toString() + '" height="' + tall.toString() + '" src="' + st + '" frameborder="0"></iframe>');
				
			}
			
			// VIMEO VIDEO
			else if(media[isOn].search("vimeo.com") !== -1) {
				
				var str = "http://player.vimeo.com/video" + media[isOn].substring(media[isOn].lastIndexOf("/"));
				
				cover.html('<iframe src="' + str + '?title=0&amp;byline=0&amp;portrait=0&amp;color=' + vimeoColor + '&amp;autoplay=1" width="' + wide.toString() + '" height="' + tall.toString() + '" frameborder="0"></iframe>');
				
			}
			
			// LOCAL VIDEO
			else {
				
				var wider = wide.toString();
				var taller = tall.toString();
				var splitter = media[isOn].split(".mp4")[0];
				
				cover.html('<video controls="controls" width="' + wider + '" height="' + taller + '" autoplay="autoplay">' + 
				'<source src="' + media[isOn] + '" type="video/mp4" /><source src="' + splitter + '.webm" type="video/webm" /><source src="' + splitter + '.ogv" type="video/ogg" />' + 
				
				'<object type="application/x-shockwave-flash" data="' + flashURL + '" width="' + wider + '" height="' + taller + '">' + 
                    
                    '<param name="movie" value="' + flashURL + '" />' + 
                    '<param name="allowScriptAccess" value="sameDomain" />' + 
					'<param name="allowFullScreen" value="true" />' + 
                    '<param name="bgcolor" value="#000000" />' + 
					'<param name="scale" value="noscale" />' +
					'<param name="wmode" value="transparent" />' +  
					'<param name="quality" value="high" />' + 
					'<param name="salign" value="tl" />' + 
					'<param name="flashvars" value="url=' + media[isOn] + '&wide=' + wider + '&tall=' + taller + '">' + 

                '</object></video>');
				
				(imgOn === 0) ? divOne.css("clip", "inherit") : divTwo.css("clip", "inherit");
				
			}
			
		}
		
		// SLIDESHOW IMAGE LOAD EVENT
		function loaded(event) {
			
			event.stopPropagation();
			
			if(!firstRun) {
				
				var direct, img = imgOn === 1 ? imgTwo : imgOne;
				
				if(isOn > wasOn) {
					
					img.css({
							
						left: 100, 
						display: "block", 
						clip: "rect(0px, " + wider + "px, " + taller + "px, " + wider + "px)"
							
					});
					
					direct = 1;
					
				}
					 
				else {
					
					img.css({
							
						left: -100, 
						display: "block", 
						clip: "rect(0px, 0px, " + taller + "px, 0px)"
							
					});
					
					direct = -1;
					
				}
					
				img.animate({left: 0, clip: "rect(0px, " + wider + "px, " + taller + "px, 0px)"}, 750, "easeInOutQuint", transDone);
				
				if(useText) {
					descs[wasOn].animate({left: (-(descs[wasOn].outerWidth()) - 20) * direct, opacity: 0}, 750, "easeInOutQuint");
					descs[isOn].css({left: (descs[isOn].outerWidth() + 20) * direct, display: "block", opacity: 0}).animate({left: 0, opacity: 1}, 750, "easeInOutQuint");
				}
				
				wasOn = isOn;
				
			}

			else {
				
				imgOne.fadeIn(750, transDone);
				firstRun = false;	
				
			}
			
			
		}
		
		// CLEAN UP PREVIOUS SLIDE
		function transDone() {
			
			if(imgOn === 0) {
			
				if(imgTwo) {
				
					imgTwo.remove();
					
				}
				
				if(!hasMedia) {
					
					if(vButton) vButton.css("display", "none");
					
				}
				else {
				
					cover.appendTo(divOne);	
					vButton.animate({opacity: 0.7}, 400);
					
				}
				
			}
			else {
			
				if(imgOne) {
					
					imgOne.remove();
					
				}
				
				if(!hasMedia) {
					
					if(vButton) vButton.css("display", "none");
					
				}
				else {
				
					cover.appendTo(divTwo);	
					vButton.animate({opacity: 0.7}, 500);
					
				}
				
			}
		
			var i = counter;
			
			while(i--) {
			
				if(i != isOn) buttons[i].click(buttonClick);
				
			}
			
			if(autoplay && readyToFire) timeout = setTimeout(nextSlide, delay);
			
			running = false;
			
		}
		
		// SLIDESHOW ITEM CLICK EVENT
		function gotoURL(event) {
		
			event.stopPropagation();
			
			(targets[isOn] === "_parent") ? window.location = links[isOn] : window.open(links[isOn]);
			
		}
		
		// AUTOPLAY GO TO NEXT SLIDE
		function nextSlide() {
			
			(isOn < iCount) ? isOn++ : isOn = 0;
			buttonClick();
			
		}
		
		// BUTTON CLICK EVENT
		function buttonClick(event) {
			
			running = true;
			
			if(typeof event !== "undefined") {
				
				if(timeout) clearTimeout(timeout);
				
				event.stopPropagation();
				
				isOn = $(event.target).data("id");
				
			}
			
			var i = counter, img = $("<img />"), div;
			
			while(i--) buttons[i].unbind("click", buttonClick);
			
			if(cover !== null) {
				
				cover.empty();
				vButton.appendTo(cover);
				
			}

			buttons[wasOn].removeClass("slide-show-button-active");
			buttons[isOn].addClass("slide-show-button-active");
			
			if(hasMedia) vButton.unbind("click", activateVideo).unbind("mouseover", vOver).unbind("mouseout", vOut);
			
			if(media[isOn] !== 0) {
				
				if(cover === null) videoButton(imgOn === 0 ? divTwo : divOne);

				vButton.css({opacity: 0, display: "block"}).mouseover(vOver).mouseout(vOut).click(activateVideo);
				
				hasMedia = true;
				
			}
			else {
			
				hasMedia = false;
				
			}
			
			divOne.css("clip", "rect(0px, " + wider + "px, " + taller + "px, 0px)");
			divTwo.css("clip", "rect(0px, " + wider + "px, " + taller + "px, 0px)");
			
			if(imgOn === 0) {
					
				imgOn = 1;
				imgOne.css("cursor", "default").unbind("click", gotoURL);
				
				imgTwo = img;
				div = divTwo;
				
			}
			else {
				
				imgOn = 0;
				imgTwo.css("cursor", "default").unbind("click", gotoURL);
				
				imgOne = img;
				div = divOne;
				
			}
			
			plusZ++;
			div.css("z-index", plusZ);
			
			img.css({position: "absolute", display: "none"}).load(loaded).appendTo(div);

			if(links[isOn] !== 0) img.css("cursor", "pointer").click(gotoURL);
				
			img.attr("src", urls[isOn]);
						
		}
		
	}
	
})(jQuery);











