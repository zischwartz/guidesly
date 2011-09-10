/*
* $ css clip animation support -- Jim Palmer
* version 0.1.2b
* idea spawned from $.color.js by John Resig
* Released under the MIT license.
*/

(function(e){e.fx.step.clip=function(a){if(a.state==0){var c;c=e(a.elem);var b=/rect\(([0-9]{1,})(px|em)[,\s]+([0-9]{1,})(px|em)[,\s]+([0-9]{1,})(px|em)[,\s]+([0-9]{1,})(px|em)\)/;c=b.test(a.elem.style.clip)?a.elem.style.clip:"rect(0px "+c.width()+"px "+c.height()+"px 0px)";a.start=b.exec(c.replace(/,/g," "));try{a.end=b.exec(a.end.replace(/,/g,""))}catch(i){return!1}}b=[];c=[];for(var g=a.start.length,h=a.end.length,f=a.start[d+1]=="em"?parseInt(e(a.elem).css("fontSize"))*1.333*parseInt(a.start[d]): 1,d=1;d<g;d+=2)b[b.length]=parseInt(f*a.start[d]);for(d=1;d<h;d+=2)c[c.length]=parseInt(f*a.end[d]);a.elem.style.clip="rect("+parseInt(a.pos*(c[0]-b[0])+b[0])+"px "+parseInt(a.pos*(c[1]-b[1])+b[1])+"px "+parseInt(a.pos*(c[2]-b[2])+b[2])+"px "+parseInt(a.pos*(c[3]-b[3])+b[3])+"px)"}})(jQuery);