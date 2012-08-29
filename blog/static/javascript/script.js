var CATEGORIES = ['News', 'Editorial', 'Rumor', 'Google', 'Apple', 'Microsoft', 'Favorites']

$(document).ready(function(){
	
	for(var i = 0; i < CATEGORIES.length; i++){
		$('#catList').append('<a href="/category/' + CATEGORIES[i] + '"><div class="' + CATEGORIES[i] + '">' + CATEGORIES[i] + '</div></a>');
	}


	$('#catList div:last').addClass('last')


	// $('#dateArchive').datepicker({
	// 	onClose: function(dateText, inst){
	// 		var month = $("#ui-datepicker-div .ui-datepicker-month :selected").val();
 //            var year = $("#ui-datepicker-div .ui-datepicker-year :selected").val();
 //            $(this).datepicker('setDate', new Date(year, month, 1));

 //            month++;

	// 		window.location = "/" + month + "/" + year
	// 	},
	// 	changeMonth: true,
	// 	changeYear: true,
	// 	dateFormat: 'MM yy',
	// 	showButtonPanel: true,
	// 	yearRange: '2011:2012'
	// });

	$('.hidden').hide()

	$(".expand").mouseover(function(){
		$('.hidden').animate({
			height: "show"
		})
	});

	$('.expand').mouseout(function(){
		$('.hidden').animate({
			height: "hide"
		})
	});



	// $('.sidebarRight a').qtip({
	//    content: ,
	//    show: 'mouseover',
	//    hide: 'mouseout',
	//    position: {
	// 	   corner: {
	// 	   		target: 'rightMiddle',
	// 	   		tooltip: 'leftMiddle'
	// 	   },

	// 	   adjust: {
	// 	   		x: -300,
	// 	   		screen: true
	// 	   	}
		
	// 	}
	// });

})