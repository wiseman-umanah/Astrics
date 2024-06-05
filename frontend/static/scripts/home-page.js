$(document).ready(() => {
    $('.bx-menu').on('click',
        function() {
            $('.nav-bar').toggle('slow');
            $('.bx-menu').toggle('slow');
            $('.bx-x').toggle('slow');
        }
    );
    $('.bx-x').on('click',
        function() {
            $('.nav-bar').toggle('slow');
            $('.bx-menu').toggle('slow');
            $('.bx-x').toggle('slow');
        }
    );

    $( ".new-image-section" ).on( "click", function() {
        $('.new-image-desc').slideToggle('slow')
        $('.new-image span').css('left', '10%');
        $('.new-image span').css('top', '10%');
    });
    $( ".img" ).on( "click", function() {
        $('.img-desc').slideToggle('slow')
        $('.img span').css('left', '10%');
        $('.img span').css('top', '10%');
    });
});
