<?php

namespace Controller;

use Representation\JsonSerializer;
use Resource;
use Resource\Match;

class Matches {

	protected $resource;
	protected $match;
	protected $json;

	public function __construct(Resource\Matches $resource, Match $match, JsonSerializer $json) {

		$this->resource = $resource;
		$this->match = $match;
		$this->json = $json;

	}

	public function get($type = 'display') {

		$matches = $this->resource->get($type, $_SESSION['summoner']);

		$this->json->serialize($matches);
	}

	public function post() {

		$match = $this->resource->post($_SESSION['summoner']);

		$this->json->serialize(
			$this->match->get($match['match'], $_SESSION['summoner'])
		);

	}

};

