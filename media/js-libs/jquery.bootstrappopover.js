(function($){
    $.BootstrapIdCounter = 0;
    $.BootstrapNextId = function(){
        $.BootstrapIdCounter++;
        return $.BootstrapIdCounter;
    };

    $.BootstrapPopover = function(el, options){
        var base = this;
        
        base.$el = $(el);
        base.el = el;
        
        base.$el.data("BootstrapPopover", base);
        
        base.init = function(){
            base.options = $.extend({},$.BootstrapPopover.defaultOptions, options);
            base.$popover = null;
            base.sig = base.$el.attr('href') + "_" + $.BootstrapNextId();

            if (base.options.tooltip_mode){
                base.$el.hover(function(event){
                    base.toggle_popover();
                },function(event){
                    base._close_popover(base.$el.getBootstrapPopover());
                });
            } else {
                base.$el.click(function(event) {
                    $(document).trigger('newPopoverOpen');
                    base.toggle_popover();
                    event.preventDefault();
                });
            }
        };

        base._open_popover = function($popover, cb) {
            base.options.before_open(base.$el, $popover);
            $popover.fadeIn(base.options.fade_in_speed, function(){
                if (cb != undefined) cb($popover);
                base.options.after_open(base.$el, $popover);
            });
        };

        base._close_popover = function($popover, cb) {
            base.options.before_close(base.$el, $popover);
            base.$popover.fadeOut(base.options.fade_out_speed, function() {
                // base.$popover.remove();
                base.$popover = null;
                
                $(window).unbind("resize."+base.sig);
                $(document).unbind("newPopoverOpen."+base.sig);
                if (cb != undefined) cb($popover);
                base.options.after_close(base.$el);
            });
        };

        base._resize = function(event){
            var $popover = event.data.$popover,
                $a = event.data.$a,
                a_offset = $a.offset(),
                a_o_width = $a.outerWidth(),
                d_width = $(document).width(),
                p_width = $popover.width(),
                p_height = $popover.height();
            
            if (a_offset.left < p_width) {
                $popover.removeClass('left');
                $popover.addClass('right');
            }

            if ($popover.hasClass('left')) {
                left = a_offset.left - 12 - p_width;
            } else {
                left = a_offset.left + a_o_width + 2;
            }

            $popover.css({left:left, top:top});
        };

        base.toggle_popover = function(){
            if (base == undefined) {
                base = arguments[0].data.base;
            }

            if (base.$popover != null) {
                base._close_popover(base.$popover);
                return;
            }
            var $popover = $(base.options.popover_html),
                $a = base.$el,
                title = $a.attr('title'),
                content = $($a.attr('href')).html(),
                a_offset = $a.offset(),
                a_o_width = $a.outerWidth(),
                d_width = $(document).width();
            
            $(".inner .title", $popover).html(title);
            $(".inner .content", $popover).html(content);
            $('body').append($popover);
            var p_width = $popover.width(),
                p_height = $popover.height();
            $popover.css({display:'none'});

            if (a_offset.left < p_width) {
                $popover.removeClass('left');
                $popover.addClass('right');
            }

            var top = a_offset.top - (p_height / 2) + 2;
            if ($popover.hasClass('left')) {
                left = a_offset.left - 12 - p_width;
            } else {
                left = a_offset.left + a_o_width + 2;
            }

            $popover.css({left:left, top:top});
            
            base._open_popover($popover);
            base.$popover = $popover;

            $(window).bind("resize."+base.sig, {$popover:$popover, $a:$a}, base._resize);
            $(document).bind("newPopoverOpen."+base.sig, {base:base}, base.toggle_popover);

        };
        
        base.init();
    };
    

// <a href="#" class="close">×</a>
//<a href=\"#\" class=\"close\">×</a> \


    $.BootstrapPopover.defaultOptions = {
        fade_out_speed: "fast",
        fade_in_speed: "fast",

        before_open: function() { return; },
        after_open: function() { return; },
        before_close: function() { return; },
        after_close: function() { return; },

        tooltip_mode: true,

// 		<a class=\"closex closer\">x</a> \

        popover_html: " \
        <div class=\"popover left\" style=\"position:absolute;top:-10000;left:-10000;\"> \
          <div class=\"arrow\"></div> \
          <div class=\"inner\"> \
            <h3 class=\"title\"></h3> \
            <div class=\"content\"> \
            </div> \
          </div> \
        </div>"
    };
    
    $.fn.bootstrapPopover = function(options){
        return this.each(function(){
            (new $.BootstrapPopover(this, options));
        });
    };
    
    // This function breaks the chain, but returns
    // the BootstrapPopover if it has been attached to the object.
    $.fn.getBootstrapPopover = function(){
        return this.data("BootstrapPopover").$popover;
    };
    
})(jQuery);

