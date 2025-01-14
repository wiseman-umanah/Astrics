$(document).ready(function () {
	let options; 
	
	$(document).on('click', '.reaction-btn', function (e) {
		e.preventDefault();

		let reaction_btn = $(this)
		let like_url = $(this).data('like_url');

		$.ajax({
			url: like_url,
			method: 'POST',
			success: function(response) {
				if (response.status == "liked") {
					reaction_btn.html('<small>Love</small> <i class="bx bxs-heart">')
				} else if (response.status == "unliked") {
					reaction_btn.html('<small>Love</small> <i class="bx bx-heart">')
				}
				reaction_btn.closest('.interactions').find('.reaction-count').html(`<small>${response.like_count} loves . ${response.comment_count} comments </small>`);
			}
		})
	});

	$(document).on('click', '.options', function(e) {
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

	$(document).on('click', '.save-btn', function (e) {
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

	$('.post_button').on('submit', function(e) {
		e.preventDefault();

		const formData = new FormData(this);

		$.ajax({
			url: 'create_post/',
			type: 'POST',
			data: formData,
			contentType: false,
			processData: false,
			success: function(response) {
				if (response.status == 200) {
					$('.posts').prepend(response.posts);
				}
			},
			error: function(xhr, status, error) {
				alert('Error uploading media: ' + error);
			}
		});
	});

	$(document).on('click', '.comment-btn', function (e) {
		e.preventDefault();

		let form = $(this).closest('form')[0];
		const form_action = form.action;

		const formData = new FormData(form);

		$.ajax({
			url: form_action,
			method: 'POST',
			data: formData,
			processData: false,
        	contentType: false,
			success: function(response, textStatus, xhr) {
				if (xhr.status == 200) {
					form.reset();
					refreshComments(16)
					console.log('Comment successful')
				} else {
					console.log('Failed')
				}
			},
			error: function(xhr, status, error) {
				console.error('AJAX Error: ' + error);
			}
		})
	});

	function refreshComments() {
		let url = $('#url').val();
		if (url) {
			$.ajax({
				url: url,
				method: 'GET',
				success: function(data) {
					$('.comments').html(data); 
				},
				error: function(xhr, status, error) {
					console.error('Error fetching comments:', error);
				}
			});
		}
	}
	
})
