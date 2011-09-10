package cj.videoplayer.events {

	import flash.events.Event;
	
	// this event toggles the full-screen for the video
	public final class VideoFsEvent extends Event {
     		
		public static const GOFULLSCREEN:String = "gofullscreen";

		public var goFull:Boolean;
		
		public function VideoFsEvent(type:String, fs:Boolean) {
		
			super(type, true);
			
			goFull = fs;
		
		}
		
		public override function clone():Event {
		
			return new VideoFsEvent(VideoFsEvent.GOFULLSCREEN, goFull);
		
		}
		
	}

}





