<?php

namespace Controller;

use Resource;

class Summoner {

	protected $model;

	public function __construct(Resource\Summoner $model) {
		$this->model = $model;
	}

	public function get($name) {
		
		$summoner = $this->model->get($name);

		header('Content-type: application/json');
		echo json_encode($summoner);

	}

};
