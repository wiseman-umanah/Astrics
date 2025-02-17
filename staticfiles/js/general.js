function hideShareLinks() {
	$('.share-links').css('display', 'none')
}

$(document).ready(function () {
	let options, share; 
	
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
		if (share) {
			share.children('.share-links').css('display', 'none');
			share = null;
		}
	});

	$(document).on('click', '.save-btn', function (e) {
		e.preventDefault();

		let post_id = $(this).parent(".options-dropdown").data('post_id');

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

	$(document).on('submit', '#newpost-form', function(e) {
		e.preventDefault();

		let form = $(this)[0];
		const form_action = form.action;
		let formData = new FormData(form);

		$.ajax({
			url: 'create_post/',
			type: 'POST',
			data: formData,
			contentType: false,
			processData: false,
			success: function(response, textStatus, xhr) {
				if (xhr.status == 200) {
					form.reset();
					refreshPost();
				} else {
					console.log("Form failed")
				}
			},
			error: function(xhr, status, error) {
				alert('Error uploading media: ' + error);
			}
		});
	});

	function refreshPost() {
		let url = $('#post-url').val();
		if (url) {
			$.ajax({
				url: url,
				method: 'GET',
				success: function(data) {
					$('.posts').html(data);
					hideShareLinks();
				},
				error: function(xhr, status, error) {
					console.error('Error fetching posts:', error);
				}
			});
		}
	}

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
					refreshComments()
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
	
	$(document).on('click', '.share-btn', function(e) {
		if (share && share[0] !== $(this)[0]) {
			share.children('.share-links').css('display', 'none');
		}

		const dropdown = $(this).children('.share-links');
		const isOpen = dropdown.css('display') === 'flex';

		dropdown.css('display', isOpen ? 'none': 'flex');

		share = isOpen ? null : $(this);

		e.stopPropagation()
	});

	$(document).on('click', '.copy-btn', function(e){
		let url = $(this).data('clipboard');
		console.log(url);
		navigator.clipboard.writeText(url);
	})

	$('.user-relationship').on('click', function (e) {
		e.preventDefault();

		const username = $(this).data('username');
		let action = $(this).data('action');
		let button = $(this);

		$.ajax({
			url: username + '/relationship/',
			method: 'GET',
			data: {action: action},
			success: function(response) {
				if (action == 'follow') {
					button.text('Unfollow');
					button.data('action', 'unfollow')
				} else {
					button.text('Follow');
					button.data('action', 'follow');
				}
				const followers = response.followers;
				const follows = response.follows;
				$('.follow-update').text(`${followers} followers | ${follows} following`);
			},
			error: function() {
				alert('An error occured. Please try again')
			}
		})
	})

	function hideLongText() {
		$('.more').each(function() {
			let descriptionText = $(this).text();
	
			if (descriptionText.length > 50) {
				$(this).closest('div').find('.seeMore').show();
				$(this).closest('div').find('.description').text(function(i, oldText) {
					return oldText + "...";
				});			
			} else {
				$(this).closest('div').find('.seeMore').hide();
			}
		});
	}

	hideLongText(); 
	
	$(document).on('click', '.seeMore', function() {
		let seeBtn = $(this);
		seeBtn.closest('div').find('.description').toggle();
		seeBtn.closest('div').find('.more').toggle();
		seeBtn.text(seeBtn.text() === 'See more' ? 'See less' : 'See more');
	});
	
	hideShareLinks();

	$(document).on('input', '#search-input', function() {
		let query = $(this).val();

		console.log(query);
		if (query.length > 2) {
			$.ajax({
				url: '/space/search/',
				data: {
					'query': query
				},
				dataType: 'json',
				method: 'GET',
				success: function(response) {
					let resultsDiv = $('#search-results');
					resultsDiv.empty();
					resultsDiv.css('display', 'flex');
	
					response.results.accounts.forEach(function(account) {
						let item = $(`
								<div class="user-result">	
									<div class="profile-div-small">
										<a href="${account.url}"><img src="${account.pic_url}" alt="Profile picture of ${account.first_name} ${account.last_name}"></a>
									</div>
									<div>
										<a href="${account.url}"><p>${account.first_name} ${account.last_name} (${account.username})</p></a>
									</div>
								</div>
							
						`);
						resultsDiv.append(item);
					});
					
					response.results.posts.forEach(function(post) {
						let item = $(`
							<a href="${post.url}">
								<div class="post-result">
									<p>${post.title}</p>
								</div>
							</a>
						`);
						resultsDiv.append(item);
					});
				},
				error: function() {
					alert('An error occured. Please try again')
				}
			})
		}
	})

	$(document).on('click', '.profile-section', function() {
		$('.dropdown-menu').toggle();
	})

	$(document).on('click', function (e) {
		if (!$(e.target).is('#search-input'))
			$('#search-results').css('display', 'none')
	});

	$('#year').text(new Date().getFullYear());

	const spacePhrases = [
		"Unveil the Secrets of the Stars",
		"Journey Through the Galaxies",
		"Embrace the Mysteries of the Cosmos",
		"Venture Beyond Our World",
		"Unlock the Wonders of the Universe",
		"Navigate the Infinite Expanse",
		"Experience the Beauty of the Night Sky",
		"Chart the Path of Celestial Bodies",
		"Discover the Marvels of Space Exploration",
		"Awaken Your Curiosity About the Universe",
		"Explore The Cosmos"
	];

    let currentPhrase = '';
	let currentIndex = 0;

	function getRandomPhrase() {
		const randomIndex = Math.floor(Math.random() * spacePhrases.length);
		return spacePhrases[randomIndex];
	}

	function displayPhrase() {
		currentPhrase = getRandomPhrase();
		currentIndex = 0;
		$('#startup-title').text(''); // Clear the title before starting
	
		appendNextWord();
	}

	function appendNextWord() {
		const words = [...currentPhrase];

		if (currentIndex < words.length) {
			$('#startup-title').append(words[currentIndex]);
			currentIndex++;
			setTimeout(appendNextWord, 100);
		} else {			
			setTimeout(() => {
				$('#startup-title').text('');
				displayPhrase();
			}, 6000);
		}
	}


	displayPhrase();

	const currentTheme = localStorage.getItem('theme');
	if (currentTheme) {
		$(':root').css('--back-color', currentTheme === 'dark' ? 'black' : 'white');
	}
	
	function applyTheme(theme) {
		if (theme === 'dark') {
			$(":root").css('--back-color', 'black');
			$(":root").css('--text-color', 'white');
			$(":root").css('--tile-color', 'rgb(24, 23, 23)');
			$(":root").css('--tile-back', '#0b0b0b');
		} else {
			$(":root").css('--back-color', 'white');
			$(":root").css('--text-color', 'black');
			$(":root").css('--tile-color', 'rgb(231, 232, 232)');
			$(":root").css('--tile-back', '#ece0e0');		
		}
	}
	
	
	function mode() {
		const currentTheme = localStorage.getItem('theme') || 'dark';
		let newTheme;
	
		if (currentTheme === 'dark') {
			newTheme = 'light';
		} else {
			newTheme = 'dark';
		}
	
		applyTheme(newTheme);
	
		localStorage.setItem('theme', newTheme);
	}
	
	const savedTheme = localStorage.getItem('theme') || 'dark';
	applyTheme(savedTheme);
	
	$('.mode-toggle').on('click', mode);
})
