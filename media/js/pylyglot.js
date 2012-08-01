(function ($) {
	$.fn.extend({
		fixedTableHeader: function(options) {
			var $self 			= $(this),
				self  			= this,
				$window 		= options.$window,
				offset			= $self.offset().top,
				$fixedWrapper 	= $('#fixedTableHeader'),
				thWidth			= $self.find('th').css('width');

			if ( $window.scrollTop() >= offset && !$('#fixedTableHeader').length ) {
				$fixedWrapper = $('<div id="fixedTableHeader"></div>').insertAfter($self);
				$fixedWrapper.append($self.clone());
				$fixedWrapper.find('th').css('width', thWidth); // force the width of each th
					
				setTimeout(function() {$fixedWrapper.find('thead').addClass('fixed');}, 0);
			} else if ( $fixedWrapper.length && $window.scrollTop() <= offset ) {
				$fixedWrapper.remove();
			}
			
			return self;
		}
	});
})(jQuery);