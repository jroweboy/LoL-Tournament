<?php

namespace Controller;

use Representation;

class App {

	protected $representation;

	public function __construct(Representation\App $representation) {
		$this->representation = $representation;
	}

	public function get() {

		$this->representation->get();

	}

};

