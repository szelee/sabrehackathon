$(document).ready(function(){
	//$(".alert").addClass("in").fadeOut(4500)
    /* swap open/close side menu icons */
	$('[data-toggle=collapse]').click(function(){
		// toggle icon
		$(this).find("i").toggleClass("glyphicon-chevron-right glyphicon-chevron-down");
	});

	$("[rel='tooltip']").tooltip();

	var from_$input = $('#time-start').pickadate();
	var from_picker = from_$input.pickadate('picker');

	var to_$input = $('#time-end').pickadate({
		date_max:2
	});
	var to_picker = to_$input.pickadate('picker');

	// Check if there�s a �from� or �to� date to start with.
	if (from_picker.get('value')) {
		to_picker.set('max', from_picker.get('select'));
		//to_picker.set('min', from_picker.get('select'));
	}
	if (to_picker.get('value')) {
		from_picker.set('max', to_picker.get('select'));
	}

	// When something is selected, update the �from� and �to� limits.
	from_picker.on('set', function (event) {
		if (event.select) {
			to_picker.set('min', from_picker.get('select'));
		}
		else if ('clear' in event) {
			to_picker.set('min', false)
		}
	})
	to_picker.on('set', function (event) {
		if (event.select) {
			from_picker.set('max', to_picker.get('select'))
		}
		else if ('clear' in event) {
			from_picker.set('max', false)
		}
	})
});

$('.thumbnail').hover(
	function () {
		$(this).find('.caption').slideDown(110); //.fadeIn(250)
	},
	function () {
		$(this).find('.caption').slideUp(110); //.fadeOut(205)
	}
);

//highlight glyphicons when it's checked
$('ul.bs-glyphicons-list li').click(function () {
	var $cb = $(this).find(":checkbox");
	if (!$cb.prop("checked")) {
		$cb.prop("checked", true).trigger('change');
		//$(this).addClass("checked_glyphicon");
	} else {
		$cb.prop("checked", false).trigger('change');
		//$(this).removeClass("checked_glyphicon");
	}
});

$('li input[type=checkbox]').change(function () {
	var $input = $(this);
	if ($input.is(":checked")) {
		$input.parent().addClass("checked_glyphicon");
	}
	else {
		$input.parent().removeClass("checked_glyphicon");
		//$('<input>').attr('type', 'hidden').attr('name', 'delete-pref[]').attr('value', $input.val()).appendTo('#prefForm');
	}
});

$('#time-start').blur(function (e) {
	if ($('#time-start').parent().hasClass('has-error')) {
		$('#time-start').parent().removeClass('has-error');
		$('#time-start').parent().children(".help-block").addClass('hide');
		$('#alert').removeClass("in");
	}
});

$('#time-end').blur(function (e) {
	if ($('#time-end').parent().hasClass('has-error')) {
		$('#time-end').parent().removeClass('has-error');
		$('#time-end').parent().children(".help-block").addClass('hide');
		$('#alert').removeClass("in");
	}
});

function validateDate(e) {
	var strReturn = true;

	if ($('#time-start').val() == '' && !$('#nodate').is(':checked')) {
		$('#time-start').parent().addClass('has-error');
		$('#time-start').parent().children(".help-block").removeClass('hide');
		e.preventDefault();
		strReturn = false;
		console.log("Error in start date");
	}
	else {
		if ($('#time-start').parent().hasClass('has-error'))
			$('#time-start').parent().removeClass('has-error');
	}

	if ($('#time-end').val() == '' && !$('#nodate').is(':checked')) {
		$('#time-end').parent().children(".help-block").removeClass('hide');
		e.preventDefault();
		$('#time-end').parent().addClass('has-error');
		strReturn = false;
	}
	else {
		if ($('#time-end').parent().hasClass('has-error'))
			$('#time-end').parent().removeClass('has-error');
	}

	return strReturn;
}

function resizeElementHeight(element, exHeight) {
	var height = heightCheck()
	element.style.height = ((height - element.offsetTop - exHeight) + "px");
}

function heightCheck() {
	var height = 0;
	var body = window.document.body;
	if (window.innerHeight) {
		height = window.innerHeight;
	}
	else if (body.parentElement.clientHeight) {
		height = body.parentElement.clientHeight;
	}
	else if (body && body.clientHeight) {
		height = body.clientHeight;
	}
	return height;
}

$('#prefForm').on('submit', function (event) {
	event.preventDefault();
	console.log("form submitted!")  // sanity check
	
	data = $(this).serializeArray();
	var preferences = [];
	$('input[name="preferences"]').each(function () {
		if ($(this).is(":checked"))
			preferences.push($(this).val());
	});
    //data = '{ "preferences[]": [' + preferences + '], "update-pref": "' + $('input[name="update-pref"]').val() + '" }';
	console.log(JSON.stringify($.param(data)));
	create_post('#prefForm', $(this).attr('method'), $(this).attr('action'), JSON.stringify($.param(data)));
});

$('#userForm').on('submit', function (event) {
    event.preventDefault();
    data = $(this).serialize();
    create_post('#userForm', $(this).attr('method'), $(this).attr('/user/profile'), data);
    $('#userForm').ajaxForm();
});

function create_post(formId, method, action, data) {
	console.log("create post is working!") // sanity check
	
	$.ajax({
		url: action, // the endpoint
		type: method, // http method
        processData: false,
		data: data, // data sent with the post request
		// handle a successful response
		success: function (html) {
		    //$('#post-text').val(''); // remove the value from the input
			var doc = $(html.responseText);
			var $form = $(formId);
			var $clone = $form.clone(true);
			$clone.html(doc.find(formId).html());
			$form.replaceWith($clone);
			if (formId == "#userForm") {
			    //update the image
			    $clone.html(doc.find('#profileImage').html());
			    $('#profileImage').replaceWith($clone);
			}
			console.log($clone); // log the returned json to the console
			console.log("success"); // another sanity check
		},
		// handle a non-successful response
		error: function (xhr, errmsg, err) {
			$('#results').html("<div class='alert-box alert radius'>Oops! We have encountered an error: " + errmsg +
				" <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
			console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
		}
	});
}



// This function gets cookie with a given name
function getCookie(name) {
	var cookieValue = null;
	if (document.cookie && document.cookie != '') {
		var cookies = document.cookie.split(';');
		for (var i = 0; i < cookies.length; i++) {
			var cookie = jQuery.trim(cookies[i]);
			// Does this cookie string begin with the name we want?
			if (cookie.substring(0, name.length + 1) == (name + '=')) {
				cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
				break;
			}
		}
	}
	return cookieValue;
}
var csrftoken = getCookie('csrftoken');

/*
The functions below will create a header with csrftoken
*/

function csrfSafeMethod(method) {
	// these HTTP methods do not require CSRF protection
	return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
function sameOrigin(url) {
	// test that a given url is a same-origin URL
	// url could be relative or scheme relative or absolute
	var host = document.location.host; // host + port
	var protocol = document.location.protocol;
	var sr_origin = '//' + host;
	var origin = protocol + sr_origin;
	// Allow absolute or scheme relative URLs to same origin
	return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
		(url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
		// or any other URL that isn't scheme relative or absolute i.e relative.
		!(/^(\/\/|http:|https:).*/.test(url));
}

$.ajaxSetup({
	beforeSend: function (xhr, settings) {
		if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
			// Send the token to same-origin, relative URLs only.
			// Send the token only if the method warrants CSRF protection
			// Using the CSRFToken value acquired earlier
			xhr.setRequestHeader("X-CSRFToken", csrftoken);
		}
	}
});


function loadevents() {
	var src = "/searchengine/events";
	$.get(src,
		{
			arrival_date: $('#time-start').val(),
			depart_date: $('#time-end').val(),
			//csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
		},
		function (html) {
			$('#right1').html(html);
		}
	);
};

function createMarker(iconurl, currentmap, mapdata) {
	if (iconurl == 0)
		iconurl = 'https://maps.google.com/mapfiles/kml/shapes/schools_maps.png';

	var marker = new MarkerWithLabel({
		position: mapdata,
		map: currentmap,
		draggable: false,
		raiseOnDrag: false,
		icon: iconurl,
		//labelAnchor: new google.maps.Point(4,35),
		labelClass: 'labels',
		labelInBackground: false
	});
	return marker;
}

$(document).ajaxSend(function (event, request, settings) {
	$('#loading-indicator').show();
});

$(document).ajaxComplete(function (event, request, settings) {
	$('#loading-indicator').hide();
});

$('#myTab').on('click', 'a[data-toggle="tab"]', function(e) {
  e.preventDefault();

  var $link = $(this);

  if (!$link.parent().hasClass('active')) {

    //remove active class from other tab-panes
    $('.tab-content:not(.' + $link.attr('href').replace('#', '') + ') .tab-pane').removeClass('active');

    // click first submenu tab for active section
    $('a[href="' + $link.attr('href') + '_all"][data-toggle="tab"]').click();

    // activate tab-pane for active section
    $('.tab-content.' + $link.attr('href').replace('#', '') + ' .tab-pane:first').addClass('active');
  }

});