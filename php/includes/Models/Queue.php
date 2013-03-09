<?php

namespace Models;

use Pdo;

class Queue {

	protected $pdo;

	public function __construct(Pdo $pdo) {
		$this->pdo = $pdo;
	}

}
