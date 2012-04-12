<?php

namespace Representation;

class JsonSerializer {

	public function serialize($data) {
		header('Content-type: application/json');
		echo json_encode($data, JSON_PRETTY_PRINT);
	}

};

