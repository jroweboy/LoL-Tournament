<?php

namespace Controller;

use Representation\JsonSerializer;
use Resource;

class Match {

	protected $resource;
	protected $json;

	public function __construct(Resource\Match $resource, JsonSerializer $json) {

		$this->resource = $resource;
		$this->json = $json;

	}

	public function get($id) {

		$match = $this->resource->get($id, $_SESSION['summoner']);

		$this->json->serialize($match);
	}

	public function post($id) {

		$match = $this->resource->post($id);

		$this->json->serialize($match);

	}

	public function delete($id) {

		$info = $this->resource->delete($id);

		$this->json->serialize($info);

	}

};

