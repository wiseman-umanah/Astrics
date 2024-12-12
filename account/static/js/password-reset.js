$(document).ready(function() {
    // Step 1: Submit email for password reset
    $('#request-reset').on('submit', function(e) {
        e.preventDefault();
        // Simulate success response
        $('#request-reset').hide();
        $('#reset-confirmation').fadeIn();
        $('#form-title').text('Check Your Email');
    });

    // Step 3: Set new password
    $('#back-login').on('click', function(e) {
		window.location.href = '/account/login'
	})
});
