package cj.videoplayer {
	
	// import flash classes
	import flash.display.Sprite;
	import flash.display.MovieClip;
	import flash.events.Event;
	import flash.events.MouseEvent;
	
	// import custom events
	import cj.videoplayer.events.ToggleEvent;
	
    public final class PlayPause extends Sprite {
		
		private var isPlaying:Boolean;
		
		// class constructor
		public function PlayPause() {

			isPlaying = false;
			this.mouseEnabled = false;
			
			playMC.buttonMode = true;
			pauseMC.buttonMode = true;
			pauseMC.visible = false;
			
			addListen();
			
		}
		
		// activate the button
		internal function addListen():void {
			
			playMC.addEventListener(MouseEvent.ROLL_OVER, over);
			playMC.addEventListener(MouseEvent.ROLL_OUT, out);
			playMC.addEventListener(MouseEvent.CLICK, switchPlay);
			
			pauseMC.addEventListener(MouseEvent.ROLL_OVER, over);
			pauseMC.addEventListener(MouseEvent.ROLL_OUT, out);
			pauseMC.addEventListener(MouseEvent.CLICK, switchPlay);
			
		}
		
		// switch to playing state
		internal function setPlay():void {
			playMC.visible = false;
			pauseMC.visible = true;
			isPlaying = true;
		}
		
		// mouse over function
		private function over(event:MouseEvent):void {
			event.currentTarget.gotoAndStop(2);
		}
		
		// mouse out function
		private function out(event:MouseEvent):void {
			event.currentTarget.gotoAndStop(1);
		}
		
		// checks the playing state
		internal function checkPause():Boolean {
			
			var checker:Boolean;
			
			(isPlaying) ? checker = true : checker = false;
			isPlaying = true;
			switchPlay();
			
			return checker;
			
		}
		
		// checks the playing state and switches it
		internal function checkPlay():void {
			
			isPlaying = false;
			switchPlay();
			
		}
		
		// toggles the playing state
		internal function switchPlay(event:MouseEvent = null):void {
			
			if(!isPlaying) {
				playMC.visible = false;
				pauseMC.visible = true;
				isPlaying = true;
			}
			else {
				pauseMC.visible = false;
				playMC.visible = true;
				isPlaying = false;
			}
			
			dispatchEvent(new ToggleEvent(ToggleEvent.TOGGLEPLAY, isPlaying));
			
		}
		
		// garbage collection
		internal function kill():void {
			
			playMC.removeEventListener(MouseEvent.ROLL_OVER, over);
			playMC.removeEventListener(MouseEvent.ROLL_OUT, out);
			playMC.removeEventListener(MouseEvent.CLICK, switchPlay);

			pauseMC.removeEventListener(MouseEvent.ROLL_OVER, over);
			pauseMC.removeEventListener(MouseEvent.ROLL_OUT, out);
			pauseMC.removeEventListener(MouseEvent.CLICK, switchPlay);
			
			playMC.removeChildAt(0);
			pauseMC.removeChildAt(0);
			
			removeChildAt(0);
			removeChildAt(0);
			
		}
		
    }
}








