package cj.videoplayer.events {

	import flash.events.Event;
	
	// this event toggles the play/pause for the video
	public final class ToggleEvent extends Event {
     		
		public static const TOGGLEPLAY:String = "toggleplay";

		public var isPlaying:Boolean;
		
		public function ToggleEvent(type:String, isPlay:Boolean) {
		
			super(type, true);
			
			isPlaying = isPlay;
		
		}
		
		public override function clone():Event {
		
			return new ToggleEvent(ToggleEvent.TOGGLEPLAY, isPlaying);
		
		}
		
	}

}





