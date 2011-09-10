package cj.videoplayer {
	
	// import flash classes
	import flash.display.Sprite;
	import flash.display.Shape;
	
	// this class draws the control bar
    public final class Shaper extends Sprite {
		
		// begin private vars
		private var left:Shape;
		private var right:Shape;
		private var center:Shape;
		private var lMask:Shape;
		private var rMask:Shape;
		private var lHolder:Sprite;
		private var rHolder:Sprite;
		// end private vars
		
		// class constructor
		public function Shaper() {
			
			this.mouseEnabled = false;
			this.mouseChildren = false;
			
			left = drawRound();
			right = drawRound();
			center = new Shape();
			
			lMask = drawMask();
			rMask = drawMask();
			
			left.mask = lMask;
			right.mask = rMask;
			
			lHolder = new Sprite();
			rHolder = new Sprite();
			
			lHolder.addChild(left);
			lHolder.addChild(lMask);
			
			rHolder.addChild(right);
			rHolder.addChild(rMask);
			
			center.x = 25;
			right.x = -25;
			
			// add children to the stage
			addChild(lHolder);
			addChild(rHolder);
			addChild(center);
			
		}
		
		// draws the mask
		private function drawMask():Shape {
			
			var sh:Shape = new Shape();
			sh.graphics.beginFill(0x000000);
			sh.graphics.drawRect(0, 0, 25, 41);
			sh.graphics.endFill();
		
			return sh;
			
		}
		
		// draws the center shape
		internal function drawCenter(w:int):void {
			
			w -= 50;
			
			center.graphics.clear();
			center.graphics.beginFill(0x000000);
			center.graphics.drawRect(0, 0, w, 41);
			center.graphics.endFill();
			
			rHolder.x = w + 25;
			
		}
		
		// draws the round corners
		private function drawRound():Shape {
			
			var sh:Shape = new Shape();
			sh.graphics.beginFill(0x000000);
			sh.graphics.drawRoundRect(0, 0, 50, 41, 10);
			sh.graphics.endFill();
			
			return sh;
			
		}
		
		// garbage collection
		internal function kill():void {
				
			lHolder.removeChild(left);
			lHolder.removeChild(lMask);
			
			rHolder.removeChild(right);
			rHolder.removeChild(rMask);
			
			removeChild(lHolder);
			removeChild(rHolder);
			removeChild(center);
			
			left.graphics.clear();
			right.graphics.clear();
			center.graphics.clear();
			lMask.graphics.clear();
			rMask.graphics.clear();
			
			left = null;
			right = null;
			center = null;
			lMask = null;
			rMask = null;
			lHolder = null;
			rHolder = null;
			
		}
		
    }
}








