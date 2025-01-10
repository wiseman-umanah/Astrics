$(document).ready(function () {
	let options; 

	$('.reaction-btn').on('click', function (e) {
		e.preventDefault();

		let post_id = $(this).data('post_id');
		let reaction_btn = $(this)

		$.ajax({
			url: 'post/' + post_id + '/like/',
			method: 'POST',
			success: function(response) {
				if (response.status == "liked") {
					reaction_btn.html('<small>Love</small> <i class="bx bxs-heart">')
				} else if (response.status == "unliked") {
					reaction_btn.html('<small>Love</small> <i class="bx bx-heart">')
				}
				$('.reaction-count').html(`<small>${response.like_count} loves</small>`)
			}
		})
	});

	$('.options').on('click', function(e) {
		if (options && options[0] !== $(this)[0]) {
			options.children('.options-dropdown').css('display', 'none');
		}

		const dropdown = $(this).children('.options-dropdown');
		const isOpen = dropdown.css('display') === 'block';

		dropdown.css('display', isOpen ? 'none': 'block');

		options = isOpen ? null : $(this);

		e.stopPropagation()
	})

	$(document).on('click', function (e) {
		if (options) {
			options.children('.options-dropdown').css('display', 'none');
			options = null;
		}
	});

	$('.save-btn').on('click', function (e) {
		e.preventDefault();

		let post_id = $(this).parent(".options-dropdown").data('post_id');
		console.log(post_id);

		let save_btn = $(this)

		$.ajax({
			url: 'post/' + post_id + '/save/',
			method: 'POST',
			success: function(response) {
				if (response.status == "added") {
					save_btn.text('Remove from Favorite')
				} else if (response.status == "removed") {
					save_btn.text('Save from Favorite')
				}
			}
		})
	});
})
