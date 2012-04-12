// use mustache.js
// use utils.js
(function($) {

	var templates = {'queue': null, 'header': null};

	var loadTemplate = function(template) {

        	$.async({
			'accept': 'application/json',
                        'method': 'GET',
                        'url':  '/assets/templates/'+ template + '.mustache',
                        'success': function(request) {
                        	console.log('Loaded: ', template);
                                templates[template] = request.responseText;
                        },
                        'error': function(request) {
                                clearInterval(timer);
                                console.log(request);
                         }
                });

	};

	var loadTemplates = function() {
		var i;
		for (i in templates) {
			loadTemplate(i);
		}
	}

	loadTemplates();

	var updateQueue = function(queue) {

		var tbody = document.getElementById('queue').firstElementChild;

		tbody.innerHTML = Mustache.render(
			templates.queue,
			{'queue': queue}
		);	

	};

	var isInQueue = function (queue) {
		var i, in_queue = false;
		for (i in queue) {

			console.log(queue[i].currentUser);

			if (queue[i].currentUser) {
				in_queue = true;
			}
		}

		console.log('in_queue:', in_queue);

		return in_queue;
	};

	var setInQueue = function(in_queue) {
		$.async({
			'accept': 'application/json',
			'method': 'POST',
			'url': '/queue',
			'data': {'in_queue':in_queue},
			'success': function(request) {
				console.log('success', request);
			},
			'error': function(request) {
				console.log('error: ', request);
			}
		});
	};


	var playPressed = function(event) {
		var id = event.target.id;
		if (id === 'play') {
			setInQueue(true);
		} else if (id === 'quit') {
			setInQueue(false);
		}
	};

	var header = document.getElementById('header');
	header.addEventListener('click', playPressed);

	var updatePlay = function(in_queue) {
		header.innerHTML = Mustache.render(
			templates.header,
			{'in_queue': in_queue}
		);

	};
	
	var update = function($) {
		$.async({
			'accept': 'application/json',
			'method': 'GET',
			'url': '/data',
			'success': function(request) {
				console.log('Updating . . . ');
				var data = JSON.parse(request.responseText);

				updateQueue(data.queue);
				updatePlay(isInQueue(data.queue));
			},
			'error': function(request) {
				console.log(request);
			}
		});
	};

	//update($);

	var timer;
	timer = setInterval(
		function(templates, update, $){

			console.log('Checking for loaded templates . . . ');

			var loaded = true, i, tmp, count = templates.length;
			
			for (i in templates) {
				if (!templates[i]) {
					loaded = false;
					break;
				}
			}

			if (loaded) {
				
				console.log('Templates loaded . . . ');

				clearInterval(timer);

				update($);

				timer = setInterval(function(update, $){
					update($);
				}, 5000, update, $);

			} else {

				console.log('Waiting on templates . . . ');

			}

		}, 100, templates, update, $
	);
	

})(utils);

