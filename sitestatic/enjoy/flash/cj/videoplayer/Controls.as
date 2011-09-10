package cj.videoplayer {
	
	// import flash classes
	import flash.display.Sprite;
	import flash.display.Shape;
	import flash.display.MovieClip;
	import flash.events.Event;
	import flash.events.MouseEvent;
	import flash.geom.Rectangle;
	
	import com.greensock.TweenLite;
	import com.greensock.easing.Quint;
	
	// import custom events
	import cj.videoplayer.events.ToggleNsEvent;
	import cj.videoplayer.events.VideoVolEvent;
	import cj.videoplayer.events.VideoLineEvent;
	
    public final class Controls extends Sprite {
		
		// begin private vars
		private var shaper:Shaper;
		private var liner:Liner;
		private var volumeMC:VolumeMC;
		private var volPercent:VolPercent;
		private var volStrip:VolStrip;
		private var lineClick:MovieClip;
		private var sLine:MovieClip;
		private var mouseTrack:MovieClip;
		private var volMask:Sprite;
		private var volShape:Shape;
		
		private var wid:int;
		private var storeW:int;
		private var trackVol:Number;
		private var stVol:String;
		private var rightSide:String;
		private var volOn:Boolean;
		private var rec:Rectangle;
		
		private var moveLine:Function;
		private var updateVol:Function;
		// end private vars
		
		// begin internal vars
		internal var playPause:PlayPause;
		internal var fullScreen:FullScreen;
		internal var theTime:TheTime;
		internal var white:MovieClip;
		internal var lineHit:MovieClip;
		internal var downMouse:Boolean;
		// end internal vars
		
		// class constructor
		public function Controls(kicker:Function, mover:Function, uVol:Function) {
			
			shaper = new Shaper();
			
			playPause = new PlayPause();
			playPause.x = 18;
			playPause.y = 13;
			
			liner = new Liner();
			liner.x = 44;
			liner.y = 15;

			moveLine = mover;
			updateVol = uVol;
			
			white = liner.wLine;
			lineHit = liner.lineB;
			lineHit.buttonMode = true;

			theTime = new TheTime();
			theTime.y = 11;
			
			kicker(theTime.txt);
			
			volumeMC = new VolumeMC();
			volumeMC.buttonMode = true;
			volumeMC.y = 11;
			
			fullScreen = new FullScreen();
			fullScreen.y = 11;
			
			volPercent = new VolPercent();
			volPercent.y = 20;
			volPercent.alpha = 0;
			
			volStrip = new VolStrip();
			volStrip.buttonMode = true;
			volStrip.alpha = 0;
			
			sLine = volStrip.sLine;
			mouseTrack = volStrip.mouseTrack;
			lineClick = volStrip.lineClick;
			
			volShape = new Shape();
			volShape.graphics.beginFill(0x000000);
			volShape.graphics.drawRect(0, 0, 20, 80);
			volShape.graphics.endFill();
			
			volMask = new Sprite();
			volMask.mouseEnabled = false;
			volMask.addChild(volShape);
			volMask.y = -50;
			
			white.mouseEnabled = white.mouseChildren = volPercent.mouseEnabled = volPercent.mouseChildren = this.mouseEnabled = false;
			volMask.cacheAsBitmap = volStrip.cacheAsBitmap = true;
			volStrip.mask = volMask;
			volShape.visible = false;
			
			// add all children to the stage
			addChild(shaper);
			addChild(playPause);
			addChild(liner);
			addChild(theTime);
			addChild(volumeMC);
			addChild(volPercent);
			addChild(volStrip);
			addChild(volMask);
			addChild(fullScreen);
			
		}
		
		// setup the control bar
		internal function setControls(w:int, duration:int):String {
			
			storeW = w;
			volOn = true;
			downMouse = false;
			trackVol = 1;
			volPercent.txt.text = "100";
			sizeControls(w);
			lineHit.scaleX = white.scaleX = 0;
			
			lineHit.addEventListener(MouseEvent.CLICK, clickLine);
			lineHit.addEventListener(MouseEvent.MOUSE_DOWN, lineDown);
			volumeMC.addEventListener(MouseEvent.ROLL_OVER, showVol);
			volumeMC.addEventListener(MouseEvent.ROLL_OUT, hideVol);
			
			volStrip.addEventListener(MouseEvent.ROLL_OVER, showVol);
			volStrip.addEventListener(MouseEvent.ROLL_OUT, hideVol);
			volStrip.clickVol.addEventListener(MouseEvent.CLICK, vClick);
			volStrip.topClick.addEventListener(MouseEvent.CLICK, tClick);
			
			volStrip.mouseEnabled = false;
			volStrip.mouseChildren = false;
			
			lineClick.addEventListener(MouseEvent.CLICK, lineClicker);
			lineClick.addEventListener(MouseEvent.MOUSE_DOWN, volDown);
			
			var min:Number = duration / 60;
			var overage:Number = min - int(min);
			var sec:int = overage * 60;
			
			min = int(min);
			
			var st1:String = min < 10 ? "0" + min : "" + min;
			var st2:String = sec < 10 ? "0" + sec : "" + sec;
			var right:String = "/" + st1 + ":" + st2;
			
			theTime.txt.text = "00:00" + right;
			
			return right;
			
		}
		
		// remove event listeners
		private function released(event:Event):void {
			
			this.parent.removeEventListener(MouseEvent.MOUSE_MOVE, enterTrack);
			stage.removeEventListener(MouseEvent.MOUSE_UP, released);
			stage.removeEventListener(Event.MOUSE_LEAVE, released);
			
			downMouse = false;
			
			dispatchEvent(new ToggleNsEvent(ToggleNsEvent.TOGGLENS, true));
			
			lineHit.addEventListener(MouseEvent.MOUSE_DOWN, lineDown);
			
		}
		
		// track video progress
		internal function enterTrack(event:MouseEvent = null):void {
			
			rec = lineHit.getBounds(this);
			
			if(mouseX > rec.x && mouseX < rec.x + rec.width) {
				white.scaleX = liner.mouseX / wid;
			}
			
			moveLine(liner.mouseX, wid);
			
		}
		
		// fires when the progress line is clicked
		private function lineDown(event:MouseEvent):void {
			
			downMouse = true;
			
			dispatchEvent(new ToggleNsEvent(ToggleNsEvent.TOGGLENS, false));
			
			lineHit.removeEventListener(MouseEvent.MOUSE_DOWN, lineDown);
			stage.addEventListener(MouseEvent.MOUSE_UP, released);
			stage.addEventListener(Event.MOUSE_LEAVE, released);
			this.parent.addEventListener(MouseEvent.MOUSE_MOVE, enterTrack);
			enterTrack();
			
		}
		
		// fires when the volume bar is released
		private function upVol(event:Event):void {
			
			this.parent.removeEventListener(MouseEvent.MOUSE_MOVE, enterVol);
			stage.removeEventListener(MouseEvent.MOUSE_UP, upVol);
			stage.removeEventListener(Event.MOUSE_LEAVE, upVol);
			
			volStrip.addEventListener(MouseEvent.ROLL_OUT, hideVol);
			lineClick.addEventListener(MouseEvent.MOUSE_DOWN, volDown);
			
			rec = lineClick.getBounds(volStrip);
			
			if(volStrip.mouseX < rec.x || volStrip.mouseX > rec.x + rec.height || volStrip.mouseY < rec.y || volStrip.mouseY > rec.y + rec.height) {
				hideVol();
			}
			
		}
		
		// hides the volume bar
		private function hideShape():void {
			volShape.visible = false;
		}
		
		// fde out the volume bar
		private function hideVol(event:MouseEvent = null):void {

			TweenLite.to(volPercent, 0.75, {alpha: 0, ease: Quint.easeOut});
			TweenLite.to(volStrip, 0.75, {alpha: 0, ease: Quint.easeOut, onComplete: hideShape});
			
			if(trackVol == 0) {
				volumeMC.gotoAndStop(3);
				volOn = false;
			}
			
			(volumeMC.currentFrame != 3) ? volumeMC.gotoAndStop(1) : null;
			
			volStrip.mouseEnabled = false;
			volStrip.mouseChildren = false;
			
		}
		
		// scrubs the video volume
		internal function enterVol(event:Event):void {
			
			rec = lineClick.getBounds(volStrip);
			
			if(volStrip.mouseY > rec.y - 1 && volStrip.mouseY - 1 < rec.y + rec.height) {
				
				trackVol = -(mouseTrack.mouseY / 42);
				sLine.scaleY = trackVol;
				stVol = String((trackVol * 100) | 0);
				volPercent.txt.text = stVol;
				updateVol(Number(stVol));
				
				if(trackVol != 0) {
					(volumeMC.currentFrame != 2) ? volumeMC.gotoAndStop(2) : null;
				}
				else {
					(volumeMC.currentFrame != 3) ? volumeMC.gotoAndStop(3) : null;
				}
				
			}
			
		}
		
		// fires when the video line is pressed
		private function volDown(event:MouseEvent):void {
			
			volStrip.removeEventListener(MouseEvent.ROLL_OUT, hideVol);
			lineClick.removeEventListener(MouseEvent.MOUSE_DOWN, volDown);
			
			stage.addEventListener(MouseEvent.MOUSE_UP, upVol);
			stage.addEventListener(Event.MOUSE_LEAVE, upVol);
			this.parent.addEventListener(MouseEvent.MOUSE_MOVE, enterVol);
			
		}

		// full-screen click
		internal function goingFull(yes:Boolean = false, sW:int = 0):void {
			
			if(yes) {
				sizeControls(sW - 40);
			}
			else {
				sizeControls(storeW);
			}
			
		}

		// fires when the video progress line is clicked
		private function lineClicker(event:MouseEvent):void {
			
			trackVol = -(mouseTrack.mouseY / 42);
			
			sLine.scaleY = trackVol;
			
			var st:String = String((trackVol * 100) | 0);
			volPercent.txt.text = st;
			
			updateVol(Number(st));
			
			volumeMC.gotoAndStop(2);
			volOn = true;
			
		}
		
		// fires when the track is clicked
		private function tClick(event:MouseEvent):void {
			
			trackVol = 1;
			volPercent.txt.text = "100";
			volumeMC.gotoAndStop(2);
			sLine.scaleY = 1;
			volOn = true;
			
		}

		// fires when the volume is clicked
		private function vClick(event:MouseEvent):void {
			
			var v:int;
			
			(trackVol == 0) ? trackVol = 1 : null;
			
			if(volOn) {
				volOn = false;
				volumeMC.gotoAndStop(3);
				sLine.scaleY = 0;
				v = 0;
			}
			else {
				volOn = true;
				volumeMC.gotoAndStop(2);
				sLine.scaleY = trackVol;
				v = trackVol * 100;
			}
			
			volPercent.txt.text = String(v);
			
			dispatchEvent(new VideoVolEvent(VideoVolEvent.VOLUMEON, volOn));
			
		}
		
		// fade in the volume
		private function showVol(event:MouseEvent):void {
			
			TweenLite.to(volPercent, 0.75, {alpha: 1, ease: Quint.easeOut});
			TweenLite.to(volStrip, 0.75, {alpha: 1, ease: Quint.easeOut});
			
			(volumeMC.currentFrame != 3) ? volumeMC.gotoAndStop(2) : null;

			volShape.visible = true;
			volStrip.mouseEnabled = true;
			volStrip.mouseChildren = true;
			
		}
		
		// dispatch an event on progress line click
		private function clickLine(event:MouseEvent):void {
			
			dispatchEvent(new VideoLineEvent(VideoLineEvent.LINECLICK, liner.mouseX, wid));
			
		}

		// toggle the play/pause
		internal function switchBack():void {
			white.scaleX = 0;
			playPause.switchPlay();
		}
		
		// position the control assets
		internal function sizeControls(w:int):void {
			
			shaper.drawCenter(w);
			wid = w - 196;
			liner.gLine.width = white.insideWhite.width = lineHit.insideLB.width = wid;
			theTime.x = wid + 58;
			volumeMC.x = theTime.x + 77;
			fullScreen.x = volumeMC.x + 25;
			
			volStrip.x = volMask.x = volumeMC.x - 3;
			volPercent.x = volumeMC.x - 10;
			
		}
		
		// garbage collection
		internal function kill():void {
			
			this.parent.removeEventListener(MouseEvent.MOUSE_MOVE, enterVol);
			
			if(stage != null) {
				stage.removeEventListener(MouseEvent.MOUSE_UP, released);
				stage.removeEventListener(Event.MOUSE_LEAVE, released);
				stage.removeEventListener(MouseEvent.MOUSE_UP, upVol);
				stage.removeEventListener(Event.MOUSE_LEAVE, upVol);
			}
			
			lineHit.removeEventListener(MouseEvent.CLICK, clickLine);
			lineHit.removeEventListener(MouseEvent.MOUSE_DOWN, lineDown);
			volumeMC.removeEventListener(MouseEvent.ROLL_OVER, showVol);
			volumeMC.removeEventListener(MouseEvent.ROLL_OUT, hideVol);
			
			volStrip.removeEventListener(MouseEvent.ROLL_OVER, showVol);
			volStrip.removeEventListener(MouseEvent.ROLL_OUT, hideVol);
			volStrip.clickVol.removeEventListener(MouseEvent.CLICK, vClick);
			volStrip.topClick.removeEventListener(MouseEvent.CLICK, tClick);
				
			lineClick.removeEventListener(MouseEvent.CLICK, lineClicker);
			lineClick.removeEventListener(MouseEvent.MOUSE_DOWN, volDown);
			
			TweenLite.killTweensOf(volPercent);
			TweenLite.killTweensOf(volStrip);
			
			playPause.kill();
			fullScreen.kill();
			shaper.kill();
			
			while(this.numChildren) {
				removeChildAt(0);
			}
			
			volShape.graphics.clear();
			
			shaper = null;
			liner = null;
			volumeMC = null;
			volPercent = null;
			volStrip = null;
			lineClick = null;
			sLine = null;
			mouseTrack = null;
			volMask = null;
			volShape = null;
			moveLine:Function;
			updateVol:Function;
			playPause = null;
			fullScreen = null;
			theTime = null;
			white = null;
			lineHit = null;
			
		}
		
    }
}








