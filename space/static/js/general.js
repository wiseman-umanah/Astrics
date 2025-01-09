$(document).ready(function () {
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
	})
})
