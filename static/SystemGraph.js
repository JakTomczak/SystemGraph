function calc_main_height() {
	var window_height = window.innerHeight;
	// alert(window_height);
	var navbar_height = document.getElementById('the_navbar').offsetHeight;
	// alert(navbar_height);
	var footer_height;
	try {
		footer_height = document.getElementById('the_footer').offsetHeight;
	}
	catch {
		footer_height = 0;
	}
	// alert(footer_height);
	var minheight = window_height - footer_height - navbar_height;
	// alert(minheight);
	document.getElementById("the_main").style.minHeight = minheight + 'px';
}

$(document).ready( function() {
	calc_main_height();
	
	$("textarea").keydown(function(e) {
		if(e.keyCode === 9) { // tab was pressed
			// get caret position/selection
			var start = this.selectionStart;
				end = this.selectionEnd;

			var $this = $(this);

			// set textarea value to: text before caret + tab + text after caret
			$this.val($this.val().substring(0, start)
						+ "\t"
						+ $this.val().substring(end));

			// put caret at right position again
			this.selectionStart = this.selectionEnd = start + 1;

			// prevent the focus lose
			return false;
		}
	});
});

$(window).bind('resize', function () { 
	calc_main_height();
});