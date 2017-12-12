$(document).ready(function() {
	// Contact
	$('#navbar-contact-item').on('click', function(event) {
		$('#contact').css('border-color', '#FF0000');
		setTimeout(function() {
			$('#contact').css('border-color', 'transparent');
		}, 1000);
	});
});

$(document).ready(function() {
	$("img").each(function(){
		var title = $(this).attr("title");
		var alt = $(this).attr("alt");
		if (alt != undefined && alt != "")
			return;
		$(this).attr("alt", title);
	})
});

/*
* FancyBox
*/
$(document).ready(function() {
	$("img.preview").each(function(){
		var title = $(this).attr("title");
		if (!title) title=$(this).attr("alt");
		var href  = $(this).data("original");
		if (href == undefined)
			href = $(this).attr("src");
		var $a    = $("<a class='preview-wrapper'></a>")
						.attr("href", href);
		if (title)
			$a.attr("title", title)
		$a.fancybox({
			openEffect	: 'none',
			closeEffect	: 'none'
		});

		$(this).wrap($a);
		if (title)
			$(this).parent().append("<span>"+title+" </span>");
	});
});
