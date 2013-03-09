(function() {

	var $ = {};

	var FormData_encode = function(json) {

		var prop, data = new FormData();
		for (prop in json) {
			data.append(prop, json[prop]);
		}

		return data;

	};

	$.async = function(options) {
		var request = new XMLHttpRequest();
		request.onreadystatechange = function(event) {

			if (request.readyState === 4) {

				if (request.status === 200) {
					options.success(request);
				} else if (options.error) {
					options.error(request);
				}

			}

		};

		if (options.error) {
			request.onerror = function(event) {
				options.error(request);
			};
		}

		request.open(
			options.method,
			options.url
		);

		request.setRequestHeader('Accept', options.accept);

		var data = FormData_encode(options.data);
		
		request.send(data);

	};

	window.utils = $;

})();
