package cj.videoplayer {
	
	// import flash classes
	import flash.display.Sprite;
	import flash.display.Shape;
	import flash.display.StageDisplayState;
	import flash.events.Event;
	import flash.events.IOErrorEvent;
	import flash.events.TimerEvent;
	import flash.events.NetStatusEvent;
	import flash.events.MouseEvent;
	import flash.events.FullScreenEvent;
	import flash.media.Video;
	import flash.media.SoundTransform;
	import flash.net.URLRequest;
	import flash.net.NetConnection;
	import flash.net.NetStream;
	import flash.text.TextField;
	import flash.text.StyleSheet;
	import flash.utils.Timer;
	import flash.geom.Point;
	import flash.ui.Mouse;
	import flash.external.ExternalInterface;
	
	// import greensock tweening engine
	import com.greensock.TweenLite;
	import com.greensock.easing.Quint;
	
	// import custom events
	import cj.videoplayer.events.ToggleEvent;
	import cj.videoplayer.events.ToggleNsEvent;
	import cj.videoplayer.events.VideoFsEvent;
	import cj.videoplayer.events.VideoVolEvent;
	import cj.videoplayer.events.VideoLineEvent;
	
    public final class SingleVideoPlayer extends Sprite {
		
		// begin private vars
		private var controls:Controls;
		private var bg:Sprite;
		private var cover:Sprite;
		private var vCover:Sprite;
		private var vHolder:Sprite;
		private var txt:TextField;
		
		private var vid:Video;
		private var meta:Object;
		private var st:SoundTransform;
		private var nc:NetConnection;
		private var ns:NetStream;
		
		private var duration:Number;
		private var place:Number;
		private var totalLoaded:Number;
		private var overage:Number;
		private var sec:Number;
		private var min:Number;
		private var bAlpha:Number;
		
		private var cw:int;
		private var ch:int;
		private var vw:int;
		private var vh:int;
		private var storeX:int;
		private var storeY:int;
		private var bColor:uint;
		
		private var st1:String;
		private var st2:String;
		private var total:String;
		
		private var full:Boolean;
		private var hasEnded:Boolean;
		private var mouseOn:Boolean;
		private var begin:Boolean;
		private var played:Boolean;
		private var playAuto:Boolean;
		private var runOnce:Boolean;
		private var wasFull:Boolean;
		private var timer:Timer;
		/// end private vars
		
		// class constructor
		public function SingleVideoPlayer() {
			
			if(stage == null) {
				addEventListener(Event.ADDED_TO_STAGE, added);
			}
			else {
				added();
			}
			
		}
		
		private function added(event:Event = null):void {
			
			if(event != null) removeEventListener(Event.ADDED_TO_STAGE, added);
			
			var url:String = root.loaderInfo.parameters["url"];
			(url == null) ? url = "video/sample.mp4" : null;
				
			var wide:String = root.loaderInfo.parameters["wide"];
			(wide == null) ? wide = "640" : null;
				
			var tall:String = root.loaderInfo.parameters["tall"];
			(tall == null) ? tall = "360" : null;
				
			vw = int(wide);
			vh = int(tall);
			
			//throw new Error("../" + url + ".mp4");
				
			setUp("../" + url);
			
		}
		
		private function setUp(str:String):void {
			
			addEventListener(Event.UNLOAD, kill);
			
			// set some initial values
			runOnce = true;
			begin = true;
			hasEnded = false;
			played = false;
			mouseOn = true;
			
			controls = new Controls(kickRef, moveLine, updateV);
			controls.x = 20;
			controls.visible = false;
			
			bg = new Sprite();
			cover = new Sprite();
			vCover = new Sprite();
			timer = new Timer(3500, 1);
			
			// create the video assets below
			st = new SoundTransform();
			
			nc = new NetConnection();
			nc.addEventListener(IOErrorEvent.IO_ERROR, catchError);
			nc.connect(null);
			
			meta = new Object();
			meta.onMetaData = runMeta;
			
			ns = new NetStream(nc);
			ns.soundTransform = st;
			ns.client = meta;
			
			vid = new Video();
			vid.attachNetStream(ns);
			
			vHolder = new Sprite();
			vHolder.mouseEnabled = false;
			vHolder.addChild(vid);
			
			// add all children to the stage
			addChild(bg);
			addChild(vHolder);
			addChild(vCover);
			addChild(controls);
			addChild(cover);
			
			ns.addEventListener(IOErrorEvent.IO_ERROR, catchError);
			ns.addEventListener(NetStatusEvent.NET_STATUS, statusEvent);
			ns.play(str);
			
			addEventListener(Event.REMOVED_FROM_STAGE, kill);
			
		}
		
		// draws the video background 
		private function drawBg():void {
			
			bg.graphics.beginFill(0);
			bg.graphics.drawRect(0, 0, vw, vh);
			bg.graphics.endFill();
			
		}
		
		// convert hex color for Flash
		private function checkPound(st:String):String {
			
			if(st.charAt(0) == "#") st = st.substr(1, 7);

			return st;
			
		}
		
		// toggles play/pause
		private function changePlay(event:ToggleEvent):void {
			
			if(event.isPlaying) {
				playVid();
			}
			else {
				pauseVid();
			}
			
		}
		
		// pauses the video
		private function pauseVid():void {
			
			removeEventListener(Event.ENTER_FRAME, updateStatus);
			played = false;
			ns.pause();
			
		}
		
		// hides the control bar
		private function fireTimer(event:TimerEvent):void {
			if(!mouseOn) {
				hideControls();
			}
		}
		
		// reactivates the control bar
		private function mover(event:MouseEvent):void {
			
			timer.stop();
			timer.start();
			
			cover.visible = false;
			
			if(controls.alpha != 1) {
				TweenLite.to(controls, 1, {alpha: 1, ease: Quint.easeOut});
			}
			
			Mouse.show();
			
			addEventListener(MouseEvent.ROLL_OUT, hideControls);
			addEventListener(Event.MOUSE_LEAVE, hideControls);
			
		}
		
		// hides the control bar
		private function hideControls(event:Event = null):void {
			
			removeEventListener(MouseEvent.ROLL_OUT, hideControls);
			removeEventListener(Event.MOUSE_LEAVE, hideControls);
			cover.visible = true;
			
			if(controls.alpha != 0) {
				TweenLite.to(controls, 1, {alpha: 0, ease: Quint.easeOut});
			}
			
			if(this.mouseX > 0 && this.mouseX < cw && this.mouseY > 0 && this.mouseY < ch) {
				Mouse.hide();
			}
			
		}
		
		// plays the video
		private function playVid():void {
			
			played = true;
			
			if(begin) {
				
				begin = false;
				
				timer.start();
				
				addEventListener(MouseEvent.MOUSE_MOVE, mover);
				addEventListener(MouseEvent.ROLL_OUT, hideControls);
				addEventListener(Event.MOUSE_LEAVE, hideControls);
				
			}
			
			addEventListener(Event.ENTER_FRAME, updateStatus);
			ns.pause();
			ns.resume();
			
		}
		
		// updates the track loaded line
		private function trackLoaded(event:Event):void {
			
			totalLoaded = ns.bytesLoaded / ns.bytesTotal;
			
			if(totalLoaded < 1) {
				controls.lineHit.scaleX = totalLoaded;
			}
			else {
				controls.lineHit.scaleX = 1;
				removeEventListener(Event.ENTER_FRAME, trackLoaded);
			}
			
		}
		
		// updates the video progress text
		private function updateStatus(event:Event):void {
			
			place = ns.time / duration;
			controls.white.scaleX = ns.time / duration;
			
			min = ns.time / 60;
			overage = min - int(min);
			sec = int(overage * 60);
			min = int(min);
			
			st1 = min < 10 ? "0" + min : "" + min;
			st2 = sec < 10 ? "0" + sec : "" + sec;
			
			txt.text = st1 + ":" + st2 + total;
			
		}
		
		// resets the video for replay
		private function resetVid():void {
			
			timer.stop();
			
			removeEventListener(Event.ENTER_FRAME, updateStatus);
			removeEventListener(MouseEvent.MOUSE_MOVE, mover);
			removeEventListener(MouseEvent.ROLL_OUT, hideControls);
			removeEventListener(Event.MOUSE_LEAVE, hideControls);
			
			cover.visible = false;
			
			if(controls.alpha != 1) {
				TweenLite.to(controls, 1, {alpha: 1, ease: Quint.easeOut});
			}
			
			Mouse.show();
						
			hasEnded = true;
			begin = true;
						
			if(played) {
				controls.switchBack();
				played = false;
			}
			
			ns.seek(0);
			ns.pause();
			
			if(txt != null) {
				txt.text = "00:00" + total;
			}
			
		}
		
		// plays the video
		private function togNS(event:ToggleNsEvent):void {
			
			if(!event.toggle) {
				
				ns.pause();
				
				if(begin) {
				
					begin = false;
					
					timer.start();
					
					this.addEventListener(MouseEvent.MOUSE_MOVE, mover);
					this.addEventListener(MouseEvent.ROLL_OUT, hideControls);
					addEventListener(Event.MOUSE_LEAVE, hideControls);
					
				}
				
			}
			else {
				removeEventListener(Event.ENTER_FRAME, updateStatus);
				controls.playPause.setPlay();
				playVid();
			}
		}
		
		// scrubs the video 
		private function moveLine(i:Number, wid:int):void {
			ns.seek(((i / wid) * duration) | 0);
		}
		
		// seeks to a new point in the video
		private function checkLine(event:VideoLineEvent):void {
			
			removeEventListener(Event.ENTER_FRAME, updateStatus);
			controls.playPause.setPlay();
			ns.seek(((event.mouseX / event.width) * duration) | 0);
			playVid();
			
		}
		
		// stores a reference to the controlbar text field
		private function kickRef(texter:TextField):void {
			txt = texter;
		}
		
		// updates the video volume
		private function updateV(vol:Number):void {
			
			st.volume = vol * .01;
			ns.soundTransform = st;
			
		}
		
		// toggles video volume on and off
		private function kickVol(event:VideoVolEvent):void {
			
			(!event.volumeOn) ? st.volume = 0 : st.volume = 1;
			ns.soundTransform = st;
			
		}
		
		// the mouse is over the control bar
		private function cOver(event:MouseEvent):void {
			mouseOn = true;
		}
		
		// the mouse is not hovering the control bar
		private function cOut(event:MouseEvent):void {
			mouseOn = false;
		}
		
		// toggles full-screen and normal screen
		private function getSizer(event:VideoFsEvent = null):void {
			
			var theW:int = vw, theH:int = vh;
			
			if(event != null) {
				
				if(event.goFull) {
					
					if(stage.displayState != StageDisplayState.FULL_SCREEN) {
						wasFull = false;
						stage.displayState = StageDisplayState.FULL_SCREEN;
					}
					else {
						wasFull = true;
					}
					
					this.x = -this.parent.localToGlobal(new Point(0, 0)).x;
					this.y = -this.parent.localToGlobal(new Point(0, 0)).y;
					
					cw = stage.stageWidth;
					ch = stage.stageHeight;
					
					var scalerH:Number = cw / vw;
					var scalerW:Number = ch / vh;
					var scaleMe:Number;
					
					if(scalerH <= scalerW) {
						scaleMe = scalerH;
					}
					else {
						scaleMe = scalerW;
					}
					
					theW *= scaleMe;
					theH *= scaleMe;
					
					vHolder.width = theW;
					vHolder.height = theH;
					
					vHolder.x = (cw >> 1) - (theW >> 1);
					vHolder.y = (ch >> 1) - (theH >> 1);
					
					bg.x = bg.y = 0;
					bg.graphics.clear();
					bg.graphics.beginFill(bColor);
					bg.graphics.drawRect(0, 0, cw, ch);
					bg.graphics.endFill();
					
					controls.x = vHolder.x + 20;
					controls.y = ch - 61;
					controls.goingFull(true, theW);
					
					full = true;
					
					stage.addEventListener(FullScreenEvent.FULL_SCREEN, escapeThis);
					bg.addEventListener(MouseEvent.ROLL_OVER, hideControls);
					
				}
				
				else {
					
					exitFull();
				
				}
			}
			else {
				
				exitFull();
				
			}
			
			vCover.graphics.clear();
			vCover.graphics.beginFill(0x000000);
			vCover.graphics.drawRect(0, 0, cw, ch);
			vCover.graphics.endFill();
			
			cover.graphics.clear();
			cover.graphics.beginFill(0x000000);
			cover.graphics.drawRect(0, 0, cw - 40, 41);
			cover.graphics.endFill();
			
			cover.x = controls.x;
			cover.y = controls.y;
			
		}
		
		// exits full-screen
		private function exitFull():void {
			
			if(full) {
			
				stage.removeEventListener(FullScreenEvent.FULL_SCREEN, escapeThis);
				
				if(!wasFull) {
					stage.displayState = StageDisplayState.NORMAL;
				}
						
				this.x = storeX;
				this.y = storeY;
						
				controls.goingFull();
				controls.x = 20;
				controls.y = vh - 61;
		
				cw = vw;
				ch = vh;
						
				vHolder.width = cw;
				vHolder.height = ch;
						
				vHolder.x = 0;
				vHolder.y = 0;
						
				bg.removeEventListener(MouseEvent.ROLL_OVER, hideControls);
				bg.x = 0;
				bg.y = 0;
				bg.graphics.clear();
				drawBg();
				
				full = false;
				
			}
			
		}
		
		// fires when the escape key is clicked
		private function escapeThis(event:FullScreenEvent):void {
			
			getSizer();
			controls.fullScreen.goNormal();
			
		}
		
		// fires when the meta data is available
		private function runMeta(info:Object):void {
			
			// we only run this function once 
			if(runOnce) {
				
				runOnce = false;
			
				ns.seek(0);
				ns.pause();
					
				cw = vw;
				ch = vh;
				
				drawBg();
					
				vid.width = vw;
				vid.height = vh;
	
				duration = info.duration;
				controls.y = vh - 61;
				
				cover.graphics.clear();
				cover.graphics.beginFill(0x000000);
				cover.graphics.drawRect(0, 0, vw - 40, 41);
				cover.graphics.endFill();

				cover.x = 20;
				cover.y = controls.y;
				cover.alpha = 0;
				cover.visible = false;
				
				vCover.graphics.clear();
				vCover.graphics.beginFill(0x000000);
				vCover.graphics.drawRect(0, 0, vw, vh);
				vCover.graphics.endFill();
				vCover.alpha = 0;
				
				total = controls.setControls(vw - 40, duration);
				controls.visible = true;
				controls.alpha = 0;
				TweenLite.to(controls, 1, {alpha: 1, ease: Quint.easeOut});
				
				// add all event listeners
				timer.addEventListener(TimerEvent.TIMER, fireTimer);
				controls.addEventListener(MouseEvent.ROLL_OVER, cOver);
				controls.addEventListener(MouseEvent.ROLL_OUT, cOut);
				addEventListener(Event.ENTER_FRAME, trackLoaded);
				
				addEventListener(ToggleEvent.TOGGLEPLAY, changePlay);
				addEventListener(ToggleNsEvent.TOGGLENS, togNS);
				addEventListener(VideoFsEvent.GOFULLSCREEN, getSizer);
				addEventListener(VideoVolEvent.VOLUMEON, kickVol);
				addEventListener(VideoLineEvent.LINECLICK, checkLine);
				
				playVid();
				controls.switchBack();
				
			}
			
		}
		
		// listen for when the video ends
		private function statusEvent(event:NetStatusEvent):void {
			
			switch(event.info.code) {
				
				case "NetStream.Play.Stop":
					
					if(!controls.downMouse) {
						resetVid();
					}
					
				break;
				
			}
		}
		
		// ctach loading errors
		private function catchError(event:IOErrorEvent):void {}
		
		// string to boolean conversion
		private function convert(st:String):Boolean {
			
			if(st.toLowerCase() == "true") {
				return true;
			}
			else {
				return false;
			}
			
		}
		
		// garbage collection
		private function kill(event:Event):void {
			
			removeEventListener(Event.UNLOAD, kill);
			removeEventListener(Event.REMOVED_FROM_STAGE, kill);
			
			if(controls != null) {
				
				removeEventListener(Event.ENTER_FRAME, trackLoaded);
				timer.removeEventListener(TimerEvent.TIMER, fireTimer);
				timer.stop();
				
				ns.removeEventListener(IOErrorEvent.IO_ERROR, catchError);
				ns.removeEventListener(NetStatusEvent.NET_STATUS, statusEvent);
				ns.close();
				vid.clear();
				
				TweenLite.killTweensOf(controls);
				
				removeEventListener(MouseEvent.ROLL_OUT, hideControls);
				removeEventListener(Event.MOUSE_LEAVE, hideControls);
				removeEventListener(MouseEvent.MOUSE_MOVE, mover);
				removeEventListener(Event.ENTER_FRAME, updateStatus);
				
				if(stage != null) {
					stage.removeEventListener(FullScreenEvent.FULL_SCREEN, escapeThis);
				}
				
				bg.removeEventListener(MouseEvent.ROLL_OVER, hideControls);
				timer.removeEventListener(TimerEvent.TIMER, fireTimer);
				controls.removeEventListener(MouseEvent.ROLL_OVER, cOver);
				controls.removeEventListener(MouseEvent.ROLL_OUT, cOut);
				removeEventListener(Event.ENTER_FRAME, trackLoaded);
					
				removeEventListener(ToggleEvent.TOGGLEPLAY, changePlay);
				removeEventListener(ToggleNsEvent.TOGGLENS, togNS);
				removeEventListener(VideoFsEvent.GOFULLSCREEN, getSizer);
				removeEventListener(VideoVolEvent.VOLUMEON, kickVol);
				removeEventListener(VideoLineEvent.LINECLICK, checkLine);
				
				Mouse.show();
				
				controls.kill();
				nc.close();
				
				vHolder.removeChild(vid);
				
				while(this.numChildren) {
					removeChildAt(0);
				}
				
				bg.graphics.clear();
				vCover.graphics.clear();
				cover.graphics.clear();
				
				controls = null;
				bg = null;
				cover = null;
				vCover = null;
				vHolder = null;
				txt = null;
				vid = null;
				meta = null;
				st = null;
				nc = null;
				ns = null;
				timer = null;
				
			}
			
		}
		
    }
}







