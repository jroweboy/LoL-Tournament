<?php

namespace Controller;

use Artax\Http\Exceptions\HttpException;
use Representation\JsonSerializer;
use Resource;

class Queue {

	protected $resource;
	protected $json;

	public function __construct(Resource\Queue $queue, JsonSerializer $json) {
		$this->resource = $queue;
		$this->json = $json;
	}

	public function get() {

		$queue = $this->resource->get();

		$this->json->serialize($queue);

	}

	public function post() {

		if (!isset($_POST['in_queue'])) {
			throw new HttpException('Bad Request: Must send boolean value `in_queue`.', 400);
		}
		
                $queue = $this->resource->post(
			$_POST['in_queue'],
			$_SESSION['summoner']
		);

		$this->json->serialize($queue);

	}

};

