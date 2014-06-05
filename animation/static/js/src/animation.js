/* Javascript for AnimationXBlock. */
function AnimationXBlock(runtime, element) {
    $(function ($) {
	// Grab XBlocks data. 
	handlerUrl = runtime.handlerUrl(element, 'update_position');
	var data = JSON.parse($(".animation_source", element).text())
	var animation = data['animation'];

	var position = data['position'];
	var max_position = data['max_position'];

	// Set the correct image and text when the slider moves. Also, 
	// make an AJAX call to the server to save position and
	// maximum position. 
	// 
	// TODO: Should we do this less often for lower load? 
	// (It's okay right now, but less would be cleaner) 
	function update_animation() {
	    position = $(".animation_slider", element).labeledslider("value")
	    $(".animation_image").attr("src", animation[position].src);
	    $(".animation_text").html(animation[position].desc);
	    if (position > max_position) { max_position = position; }
	    if (max_position == animation.length-1) {
		$('.animation_wrapper', element).addClass("animation_done");
	    }
	    $.ajax({
		type: "POST",
		url: handlerUrl,
		data: JSON.stringify({"position" : position, 
				      "max_position" : max_position}),
	    });
	}

	// Initialize slider. On any change, update the state
	$( ".animation_slider", element ).labeledslider({
	    value: position, 
	    min: 0, 
	    max: animation.length-1, 
	    step: 1, 
	    stop: function( event, ui) { update_animation(); },
	    slide: function( event, ui) { update_animation(); },
	    change: function( event, ui) { update_animation(); }
	});

	// Go to current position in animation
	update_animation();

	$(".animation_left", element).click(function(){
	    new_position = position-1;
	    if(new_position<0) {
		new_position = 0;
	    }
	    $(".animation_slider", element).labeledslider("value", new_position);
	});

	$(".animation_right", element).click(function(){
	    new_position = position + 1;
	    if(new_position > animation.length - 1) {
		new_position = animation.length - 1;
	    }
	    $(".animation_slider", element).labeledslider("value", new_position);
	});

	// Preload images. I'm not sure this works. Internet 
	// said it did, but I think it might not, just from 
	// performance
	for(i=0; i<animation.length; i++){
	    animation[position]["image"] = new Image();
	    animation[position]["image"].src = animation[position].src;
	}
    });
}