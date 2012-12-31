$(document).ready(function(){

	// Previews content from html content
	// box
	function updatePreview(){
		var input = $("#id_content").val();
		var title = input.search('<h1>');
		var endTitle = input.search('</h1>');
		if(title != -1 && endTitle != -1){
			var title = input.substring(title+ 4, endTitle );
			$('#id_title').val(title);
			$('.titleBox').html('<h1>' + title + '</h1>');
			input = input.substring(endTitle + 5);
			$('#id_content').val(input);
		}

		var sourceStart = input.search('<p>Source: ');
		var endSource = input.search('</p>', sourceStart);
		if(sourceStart != -1 && endSource != -1){
			
			var source = input.substring(sourceStart + 11, endSource);
					$('.titleBox h1').wrap('<a target="_blank" href=' + source + ' />');
			$('#id_sourceUrl').val(source);
			input = input.substring(endSource + 5);
			$('#id_content').val(input);
		}
		$('.preview').html(input);
	}

	// Updates the title in preview,
	// with text from title box
	function updateTitle(){
		var title = $('#id_title').val();
		$('.titleBox').html('<h1>' + title + '</h1>');
	}

	function updateSource(){
		var source = $('#id_sourceUrl').val();
		$('.titleBox h1').wrap('<a target="_blank" href=' + source + ' />');
		
	}

	// Updates in case content was alreadly loaded into form
	updatePreview();


	$('#id_content').keyup(function(){
		updatePreview();
		

	});

	$('#id_content').change(function(){
		updatePreview();
	});

	$('#id_title').keyup(function(){
		updateTitle();
	});

	$('#id_title').change(function(){
		updateTitle();
	});

	$('#id_sourceUrl').keyup(function(){
		updateSource();
	});

	$('#id_sourceUrl').change(function(){
		updateSource();
	});

	$('.sidebarLink').removeClass('active');

	$('#newpost').addClass('active');

	updateTitle();

	updateSource();
	

});