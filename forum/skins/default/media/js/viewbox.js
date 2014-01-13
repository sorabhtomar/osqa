/*
	Programmer: Lukasz Czerwinski
	CodeCanyon: http://codecanyon.net/user/Lukasz_Czerwinski?ref=Lukasz_Czerwinski
	
	If this script you like, please put a comment on codecanyon.
	
*/
(function($){
	$.fn.viewbox = function(settings) {
		//Defaults settings  
		settings = $.extend({
			Speed		: 400,		//Speed animations
			heightWindow: 450,		//Height window
			widthWindow	: 650,		//Width window
			arrayEl		: [],		//Array with elements	
			arrayActEl	: 0,		//Array with active element		
			ajaxSuccess	: 0,		//(false) You can add new instruction ajaxSuccess
			titleThumb	: 1,		//(true) Titlebar
			navigation	: 1,		//(true) Navigation (arrows)
			keyboard	: 1,		//(true) Keyboard
			keyClose	: "c",		//(string) Key to close
			keyPrev		: "p",		//(string) Key to previous element
			keyNext		: "n",		//(string) Key to next element
			numberEl	: 1			//(true) Number elements
		}, settings);
		
		var el = $(this);
		var scroll;
		//Click
		function _clickEl () {
			_viewbox(this, el);
			return false;
		} 
		//ViewBox Function
		function _viewbox (ElClicked, el) {
			//Resetting
			settings.arrayEl.length = 0;
			settings.arrayActEl = 0;
			//if is only one element
			if ( el.length == 1) { 
				settings.arrayEl.push(new Array (
					ElClicked.getAttribute("href"), 	//[0] location
					ElClicked.getAttribute("title"), 	//[1] title
					$(ElClicked).children("img").attr("alt") //[2] description
				));
			} else {
				//If is more element
				for (var i = 0; i < el.length; i++) {
					settings.arrayEl.push(new Array (
						el[i].getAttribute("href"),  //[i] location
						el[i].getAttribute("title"), //[i] title
						$(el[i]).children("img").attr("alt") //[i] description
					));
				}
			}
//			//Add the elements to the array, but not active
			while (settings.arrayEl[settings.arrayActEl][0] != ElClicked.getAttribute("href")) {
				settings.arrayActEl++;
			}
			createView(); 
		}
		//Create
		function createView () {
			//create structure
			$("body").append("<div id='viewbox'></div><div class='vb_wrap'><div class='section_vb'><div class='close'><a href='#'>close</a></div><div class='next'><a href='#'> Next</a></div><div class='prev'><a href='#'>Previous</a></div></div>");
			$("#viewbox, .vb_wrap, .vb_wrap .section_vb, .vb_wrap .section_vb .next, .vb_wrap .section_vb .prev").hide();
				//If is set navigation
				if (settings.navigation) {
					NextAndPrev();
				}
				$(".vb_wrap .prev").unbind().bind("click", function () {
					Prev();
					return false;
				});
				$(".vb_wrap .next").unbind().bind("click", function () {
					Next();
					return false;
				});
				keyboardNav();
				
			$("#viewbox").css("opacity", 0.7).fadeIn(settings.Speed/1.6, function () {
				//Get browser size
				arraySizeBrowser = sizeBrowser();
				
				if($(document).scrollTop() == 0) {
						if (settings.heightWindow > arraySizeBrowser[0] * 1.3) {
							scroll = arraySizeBrowser[0]/9;
						} else {
							scroll = arraySizeBrowser[0]/2.2;
						}
					
				} else {
					scroll = $(document).scrollTop()+arraySizeBrowser[0]/2.3;
				} 
				//Window position
				$(".vb_wrap").css({
					top			: scroll+(settings.heightWindow/2),
					left		: arraySizeBrowser[1]
				});
				//Window animation
				$(".vb_wrap").fadeIn(settings.Speed/1.2, function () {
					$(this).animate({
						height		: settings.heightWindow,
						width		: settings.widthWindow,
						top			: scroll,
						left		: arraySizeBrowser[1]-settings.widthWindow/2
					}, settings.Speed/1.2, function () {
						//Dowload the elemment
						setElement();
						$(".vb_wrap .section_vb").delay(290).fadeIn(settings.Speed/1.5);
					});	
				}); 
			});
			//Close the ViewBox
			$("#viewbox, .vb_wrap .section_vb .close a").click(function () {
				closeWindow();
				return false;
			});
		}		
		//Set the elemments
		function setElement () { 
					//If youtube
					if(nYT(settings.arrayEl[settings.arrayActEl][0])) {
						Film(settings.arrayEl[settings.arrayActEl][0]);
					} 
					//If Vimeo
					if(nV(settings.arrayEl[settings.arrayActEl][0])){
						Vimeo(settings.arrayEl[settings.arrayActEl][0]);
					}
		}
		
	//extensions of files 
		function nYT(hrefLink) {
			return (hrefLink.indexOf("youtube.com") > 0) || (hrefLink.indexOf("youtu.be") > 0);
		}
		function nV(hrefLink) {
			return hrefLink.indexOf("vimeo") > 0;
		}
		   
	//YouTube
	function Film (hrefFilm) {
		$(".vb_wrap .section_vb").append("<div class='object'></div>"); 
		//YouTube links
		var hrefY = hrefFilm;
		
		var m = hrefFilm.match(/[&\/\?]v=(\w+)/);
		if (m == null) { m = hrefFilm.match(/youtu\.be\/(\w+)/i); }
		if (m != null) { hrefY = "http://www.youtube.com/v/" + m[1] + "&autoplay=1&loop=1&feature=related&showsearch=0"; }
		  
		$(".vb_wrap .object").append("<object width='"+settings.widthWindow+"' height='"+settings.heightWindow+"'><param name='movie' value='"+hrefY+"'></param><param name='allowFullScreen' value='true'></param><param name='allowscriptaccess' value='always'></param><embed src='"+hrefY+"' type='application/x-shockwave-flash' allowscriptaccess='always' allowfullscreen='true' width='"+settings.widthWindow+"' height='"+settings.heightWindow+"'></embed></object>"); 
	} 
	//Next/Previous elemment
	function NextAndPrev () { 
		//previous elemment
		if (settings.arrayActEl != 0) {
			$(".vb_wrap .prev").css("top", settings.heightWindow/2).show();
		} else {
			$(".vb_wrap .prev").hide();
		}
		//Next elemment
		if (settings.arrayActEl != settings.arrayEl.length-1) {
			$(".vb_wrap .next").css("top", settings.heightWindow/2).show();
		} else {
			$(".vb_wrap .next").hide();
		}
		NumberElement();
	}
	
	//Vimeo
	function Vimeo (link) {
		$(".vb_wrap .section_vb").append("<div class='object'></div>"); 
		hrefV = link.substring(21, 29);  
		$(".vb_wrap .object").append("<object width='"+settings.widthWindow+"' height='"+settings.heightWindow+"'><param name='allowfullscreen' value='true' /><param name='allowscriptaccess' value='always' /><param name='movie' value='http://vimeo.com/moogaloop.swf?clip_id="+hrefV+"&amp;server=vimeo.com&amp;show_title=1&amp;show_byline=1&amp;show_portrait=0&amp;color=&amp;fullscreen=1' /><embed src='http://vimeo.com/moogaloop.swf?clip_id="+hrefV+"&amp;server=vimeo.com&amp;show_title=1&amp;show_byline=1&amp;show_portrait=0&amp;color=&amp;fullscreen=1' type='application/x-shockwave-flash' allowfullscreen='true' allowscriptaccess='always' width='"+settings.widthWindow+"' height='"+settings.heightWindow+"'></embed></object>");  
	}
	
		
		//Support for keyboard
		function keyboardNav () {
			if(settings.keyboard) {
				$(document.documentElement).unbind().bind("keyup", function (event) {
					//IE
					if ($.browser.msie) {
						codeAscii = event.keyCode;
					} else {
						codeAscii = event.keyCode;
					}
					KeyCode = String.fromCharCode(codeAscii).toLowerCase();
					
					//Left
					if(event.keyCode == 37 || KeyCode == settings.keyPrev) {
						Prev();
					}
					//Right
					if(event.keyCode == 39 || KeyCode == settings.keyNext) {
						Next();
					}
					//ESC
					if(event.keyCode == 27 || KeyCode == settings.keyClose) {
						closeWindow();
					}
				});
			}
	}
		//previous
		function Prev () {
			if (settings.arrayActEl != 0) {
				$(".vb_wrap .section_vb").fadeOut(settings.Speed / 1.4, function(){
					$(".vb_wrap .section_vb .image, .section_vb .object").remove();
					settings.arrayActEl = settings.arrayActEl - 1;
					NumberElement();
					setElement();
					$(this).fadeIn(settings.Speed / 1.2);
					NextAndPrev();
				});
			}
		}
		//Next
		function Next () {
			if (settings.arrayActEl != settings.arrayEl.length - 1) {
				$(".vb_wrap .section_vb").fadeOut(settings.Speed / 1.4, function(){
					$(".vb_wrap .section_vb .image, .vb_wrap .section_vb .object").remove();
					settings.arrayActEl = settings.arrayActEl + 1;
					NumberElement();
					setElement();
					$(this).fadeIn(settings.Speed / 1.2);
					NextAndPrev();
				});
			}
		}
		//Numbers
		function NumberElement () {
			if(settings.numberEl) {
				$(".vb_wrap .section_vb .number").remove();
				if(settings.arrayEl.length != 0) {
					function Words () {
						//If youtube
						if(nYT(settings.arrayEl[settings.arrayActEl][0]) || nV(settings.arrayEl[settings.arrayActEl][0])) {
							return "Film ";
						} 
					}
					$(".vb_wrap .section_vb").append("<div class='number'>"+Words()+(settings.arrayActEl+1)+" / "+settings.arrayEl.length+"</div>");
				}
			}
		}
	//Change size
	function resizeWindow (Height, Width, Callback) {
		//Get the size
		var contentHeight = $(".vb_wrap").height();
		var contentWidth = $(".vb_wrap").width();
		$(".vb_wrap").animate({
			left		: document.documentElement.clientWidth/2-Width/2,
			top			: topToresize(Height, Width),
			width		: Width,
			height		: Height
		}, settings.Speed/1.5);
			$(".vb_wrap img").attr({
				height	: Height,
				width	: Width
			});
			$(".vb_wrap .image").hide().delay(settings.Speed/1.1).fadeIn(300);
		$(".vb_wrap .next, .vb_wrap .prev").css("top", Height/2);
	}
	function topToresize (Height, Width) {
		if(Height+ arraySizeBrowser[0]/2.3 > arraySizeBrowser[0]*2) {
			return $(document).scrollTop()+(arraySizeBrowser[0]/9);
		} else {
			return $(document).scrollTop()+(arraySizeBrowser[0]/2);
		}
	}
		//Close function 
		function closeWindow () {
			var arrPageSize = sizeBrowser();

			settings.arrayEl.length = 0;
			settings.arrayActEl = 0;
			$(".vb_wrap .section_vb").fadeOut(settings.Speed/1.6, function () {
				$(".vb_wrap").animate({
					left	: arrPageSize[1],
					top		: arrPageSize[0]/2+scroll,
					height	: 50,
					width	: 50
				}, settings.Speed/1.3, function () {
					$(this).fadeOut(settings.Speed/1.2, function () {
						$(this).remove();
						$("#viewbox").fadeOut(settings.Speed/1.5, function () {
							$("#viewbox").remove(); 
						});
					});
				});
			});
			
		}
		//Browser
		function sizeBrowser () {
			var arraySize = new Array;
			//Height
			arraySize[0] = document.documentElement.clientHeight/2;
			//Width 
			arraySize[1] = document.documentElement.clientWidth/2; 
			return arraySize;
		}
		
		//Thumbs
		if(settings.titleThumb) {
			jQuery.each(el, function() {
				var titleThumb = $(this).attr("title");
					if(titleThumb != "") {
						$(this).children("img").parent("a").wrap("<div class='thumbdiv'></div>");
							$(this).parent(".thumbdiv").append("<div class='title'>"+titleThumb+"</div>");
							$(this).parent(".thumbdiv").children(".title").hide();
					}
			});
			$(".thumbdiv").hover(
				function(){
					$(this).children(".title").stop(true, true).delay(150).slideDown(200);
				},
				function(){
					$(this).children(".title").stop(true, true).delay(150).slideUp(200);
				}
			);
		}
		//Click 
		return this.unbind('click').click(_clickEl); 
	};
})(jQuery); //The end 