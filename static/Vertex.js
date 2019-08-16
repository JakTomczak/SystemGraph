var LeftSidebar = true;
var RightSidebar = true;
var UpperSidebar = true;
var LowerSidebar = true;
var vertbars_min_height = 70;

function calc_max_height() {
	var window_height = window.innerHeight;
	var vertbars_height = 0;
	if (UpperSidebar) {
		vertbars_height += vertbars_min_height
	}
	if (LowerSidebar) {
		vertbars_height += vertbars_min_height
	}
	var vertbutts_height = 0;//2 * document.getElementById("lower_showhide").offsetHeight;
	var navbar_height = document.getElementById('the_navbar').offsetHeight;
	var maxheight = window_height - vertbars_height - vertbutts_height - navbar_height;
	document.getElementById("the_innerframe").style.maxHeight = maxheight + 'px';
	
}

function calc_min_height() {
	var butt_height = document.getElementById('right_showhide').offsetHeight;
	var menu_height = document.getElementById('vv_the_menu_wrapper').offsetHeight;
	var minheight = butt_height + 2*menu_height;
	document.getElementById("the_innerframe").style.minHeight = minheight + 'px';
}

function calc_cframe_margin() {
	// var leftnavbarwidth = document.getElementById('vv_navbar_left').offsetWidth;
	// var rightnavbarwidth = document.getElementById('vv_navbar_right').offsetWidth;
	// var margin = 8;
	// document.getElementById("the_central_frame").style.marginLeft = (leftnavbarwidth + margin) + 'px';
	// document.getElementById("the_central_frame").style.marginRight = rightnavbarwidth + 'px';
	try {
		document.getElementById("vv_prev_menu_dropdown").style.bottom = document.getElementById("vv_prev_menu_btn").offsetHeight + 'px';
	}catch {}
	try {
		document.getElementById("vv_next_menu_dropdown").style.bottom = document.getElementById("vv_next_menu_btn").offsetHeight + 'px';
	}catch {}
}

function calc_hidden_right_dropdown(side) {
	var dropdown = null;
	try {
		dropdown = document.getElementById("vv_more_" + side + "_menu_dropdown");
	}catch {}
	var height;
	if (dropdown) {
		dropdown.style.display = 'block';
		height = dropdown.clientHeight;
		dropdown.removeAttribute("style");
		button_height = document.getElementById("vv_more_" + side + "_menu_btn").offsetHeight;
		dropdown.style.bottom = ((button_height-height)/2) + 'px';
	}
}

$(document).ready(function() {
	document.getElementById("upper_sidebar").style.minHeight = vertbars_min_height + 'px';
	document.getElementById("lower_sidebar").style.minHeight = vertbars_min_height + 'px';
	calc_max_height();
	calc_min_height();
	calc_cframe_margin();
	calc_hidden_right_dropdown("right");
	calc_hidden_right_dropdown("left");
});

function Left_Show_Hide() {
	if (LeftSidebar) {
		document.getElementById("left_sidebar").style.display = "none";
		LeftSidebar = false;
	}
	else {
		document.getElementById("left_sidebar").style.display = "flex";
		LeftSidebar = true;
	}
}

function Right_Show_Hide() {
	if (RightSidebar) {
		document.getElementById("right_sidebar").style.display = "none";
		RightSidebar = false;
	}
	else {
		document.getElementById("right_sidebar").style.display = "flex";
		RightSidebar = true;
	}
}

function Upper_Show_Hide() {
	if (UpperSidebar) {
		document.getElementById("upper_sidebar").style.display = "none";
		UpperSidebar = false;
	}
	else {
		document.getElementById("upper_sidebar").style.display = "flex";
		UpperSidebar = true;
	}
	calc_max_height();
}

function Lower_Show_Hide() {
	if (LowerSidebar) {
		document.getElementById("lower_sidebar").style.display = "none";
		LowerSidebar = false;
	}
	else {
		document.getElementById("lower_sidebar").style.display = "flex";
		LowerSidebar = true;
	}
	calc_max_height();
}



$(window).bind('resize', function () { 
	calc_max_height();
});