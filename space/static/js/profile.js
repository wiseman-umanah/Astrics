
$(document).ready(function () {
	console.log("hello");
    $('#editProfile').on('click', function (e) {
        e.stopPropagation();
        if ($('.edit-section').css('display') === 'none') {
            $('.edit-section').css('display', 'flex');
            $('.image-div, .container').css('filter', 'brightness(20%)');
        }
    });

    $(document).on('click', function (e) {
        if (
            !$(e.target).is('#change-password') &&
            !$(e.target).closest('.edit-user-password').length
        ) {
            $('.edit-user-password').css('display', 'none');
            $('.edit-section').css('filter', 'brightness(100%)');
        }
        if (
            !$(e.target).closest('.edit-section').length &&
            !$(e.target).is('#editProfile')
        ) {
            $('.edit-section').css('display', 'none');
            $('.image-div, .container').css('filter', 'brightness(100%)');
        }
    });

    $('.edit-section').on('click', function (e) {
        e.stopPropagation();
    });

    $('#change-password').on('click', function () {
        if ($('.edit-user-password').css('display') === 'none') {
            $('.edit-user-password').css('display', 'flex');
            $('.edit-section').css('filter', 'brightness(20%)');
        }
    });

    $('.edit-section input').on('focus', function () {
        if ($('.edit-user-password').css('display') === 'flex') {
            $('.edit-user-password').css('display', 'none');
            $('.edit-section').css('filter', 'brightness(100%)');
        }
    });

    $('.edit-user-password input').on('focus', function (e) {
        e.stopPropagation();
    });

	$('#id_cover_pic').on('change', function (e) {
		if (this.files && this.files[0]) {
			var file = this.files[0];
			if (file.type.startsWith('image/')) { 
				var reader = new FileReader();
	
				reader.onload = function (e) {
					$('#cover-tag').attr('src', e.target.result);
				};
				reader.readAsDataURL(file);
			} else {
				alert("Please select a valid image file.");
			}
		}
	});

	$('#id_profile_pic').on('change', function (e) {
		if (this.files && this.files[0]) {
			var file = this.files[0];
			if (file.type.startsWith('image/')) { 
				var reader = new FileReader();
	
				reader.onload = function (e) {
					$('#profile-tag').attr('src', e.target.result);
				};
				reader.readAsDataURL(file);
			} else {
				alert("Please select a valid image file.");
			}
		}
	});
});
