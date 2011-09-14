package cj.videoplayer {
	
	// import flash classes
	import flash.display.Sprite;
	import flash.display.MovieClip;
	import flash.events.Event;
	import flash.events.MouseEvent;
	
	// import custom events
	import cj.videoplayer.events.VideoFsEvent;
	
	// this class is for the FullScreen button
    public final class FullScreen extends Sprite {
		
		// class constructor
		public function FullScreen() {
			
			this.mouseEnabled = false;
				
			fs.buttonMode = true;
			ns.buttonMode = true;
			ns.visible = false;
			
			addListen();
			
		}
		
		// activate the button
		internal function addListen():void {
			
			fs.addEventListener(MouseEvent.ROLL_OVER, over);
			fs.addEventListener(MouseEvent.ROLL_OUT, out);
			fs.addEventListener(MouseEvent.CLICK, goFull);

			ns.addEventListener(MouseEvent.ROLL_OVER, over);
			ns.addEventListener(MouseEvent.ROLL_OUT, out);
			ns.addEventListener(MouseEvent.CLICK, goNormal);
			
		}
		
		// mouse over function
		private function over(event:MouseEvent):void {
			event.currentTarget.gotoAndStop(2);
		}
		
		// mouse out function
		private function out(event:MouseEvent):void {
			event.currentTarget.gotoAndStop(1);
		}
		
		// full-screen click
		private function goFull(event:MouseEvent):void {
			
			fs.visible = false;
			ns.visible = true;
			
			dispatchEvent(new VideoFsEvent(VideoFsEvent.GOFULLSCREEN, true));
		}
		
		// normal screen click
		internal function goNormal(event:MouseEvent = null):void {
			
			ns.visible = false;
			fs.visible = true;
			
			dispatchEvent(new VideoFsEvent(VideoFsEvent.GOFULLSCREEN, false));
		}
		
		// grarbage collection
		internal function kill():void {
			
			fs.removeEventListener(MouseEvent.ROLL_OVER, over);
			fs.removeEventListener(MouseEvent.ROLL_OUT, out);
			fs.removeEventListener(MouseEvent.CLICK, goFull);
				
			ns.removeEventListener(MouseEvent.ROLL_OVER, over);
			ns.removeEventListener(MouseEvent.ROLL_OUT, out);
			ns.removeEventListener(MouseEvent.CLICK, goNormal);
			
			fs.removeChildAt(0);
			ns.removeChildAt(0);
			
			removeChildAt(0);
			removeChildAt(0);
			
		}
		
    }
}








