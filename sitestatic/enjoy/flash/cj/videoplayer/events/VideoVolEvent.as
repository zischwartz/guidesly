package cj.videoplayer.events {

	import flash.events.Event;
	
	// this event fires when the volume button is clicked
	public final class VideoVolEvent extends Event {
     		
		public static const VOLUMEON:String = "volumeon";

		public var volumeOn:Boolean;
		
		public function VideoVolEvent(type:String, vOn:Boolean) {
		
			super(type, true);
			
			volumeOn = vOn;
		
		}
		
		public override function clone():Event {
		
			return new VideoVolEvent(VideoVolEvent.VOLUMEON, volumeOn);
		
		}
		
	}

}





