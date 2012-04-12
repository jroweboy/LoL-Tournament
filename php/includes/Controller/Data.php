<?php

namespace Controller;

use Representation\JsonSerializer;
use Resource;

class Data {

	protected $queue;
	protected $matches;
	protected $json;

	public function __construct(Resource\Queue $queue, Resource\Matches $matches, JsonSerializer $json) {
		$this->queue = $queue;
		$this->matches = $matches;
		$this->json = $json;
	}

	public function get() {

		$data = [];

		$data['queue'] = $this->queue->get();

		foreach ($data['queue'] as $key => $summoner) {
			
			if ($summoner['summoner'] == $_SESSION['summoner']) {
				$data['queue'][$key]['currentUser'] = TRUE;
			}

		}

		$data['matches'] = $this->matches->get('display', $_SESSION['summoner']);

		$data['activeMatches'] = $this->matches->get('active', $_SESSION['summoner']);

		$this->json->serialize($data);

	}

};

