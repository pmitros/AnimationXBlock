/* Javascript for AnimationXBlock. */
function AnimationXBlock(runtime, element) {
    $(function ($) {
	function update_animation() {
	    $(".animation_image").attr("src", animation[$(".animation_slider").slider("value")].src);
	    $(".animation_text").html(animation[$(".animation_slider").slider("value")].desc);

	}
	var animation = JSON.parse($(".animation_source", element).text());
	$( ".animation_slider", element ).slider({
	    value: 0, 
	    min: 0, 
	    max: animation.length-1, 
	    step: 1, 
	    stop: function( event, ui) { update_animation(); },
	    slide: function( event, ui) { update_animation(); },
	    change: function( event, ui) { update_animation(); }
	});
	update_animation();
    });
}