package cj.videoplayer.events {

	import flash.events.Event;
	
	// this event toggles the play/pause for the video
	public final class ToggleNsEvent extends Event {
     		
		public static const TOGGLENS:String = "togglens";

		public var toggle:Boolean;
		
		public function ToggleNsEvent(type:String, tog:Boolean) {
		
			super(type, true);
			
			toggle = tog;
		
		}
		
		public override function clone():Event {
		
			return new ToggleNsEvent(ToggleNsEvent.TOGGLENS, toggle);
		
		}
		
	}

}





