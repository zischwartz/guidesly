package cj.videoplayer.events {

	import flash.events.Event;
	
	// this event fires when the progress line is clicked
	public final class VideoLineEvent extends Event {
     		
		public static const LINECLICK:String = "lineclick";

		public var mouseX:Number;
		public var width:int;
		
		public function VideoLineEvent(type:String, xMouse:Number, wid:int) {
		
			super(type, true);
			
			mouseX = xMouse;
			width = wid;
		
		}
		
		public override function clone():Event {
		
			return new VideoLineEvent(VideoLineEvent.LINECLICK, mouseX, width);
		
		}
		
	}

}





