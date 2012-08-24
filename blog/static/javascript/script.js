/*Licensed to the Apache Software Foundation (ASF) under one
or more contributor license agreements.  See the NOTICE file
distributed with this work for additional information
regarding copyright ownership.  The ASF licenses this file
to you under the Apache License, Version 2.0 (the
"License"); you may not use this file except in compliance
with the License.  You may obtain a copy of the License at

 http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing,
software distributed under the License is distributed on an
"AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
KIND, either express or implied.  See the License for the
specific language governing permissions and limitations
under the License.*/

var CATEGORIES = ['News', 'Editorial', 'Rumor', 'Google', 'Apple', 'Microsoft', 'Favorites']

$(document).ready(function(){
	
	for(var i = 0; i < CATEGORIES.length; i++){
		$('#catList').append('<a href="/category/' + CATEGORIES[i] + '"><div id="' + CATEGORIES[i] + '">' + CATEGORIES[i] + '</div></a>');
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