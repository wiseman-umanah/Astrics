$(document).ready(() => {
    $('.bxs-heart').on('click',
        function() {
            $(this).toggleClass('select')
        }
    );

    $(".img").on("click", function() {
		$(this).closest(".img-section").find(".img-desc").slideToggle('slow');
		
		$(this).find('span').toggleClass('move')
	});
	
	
	$('#year').text(new Date().getFullYear());
});
