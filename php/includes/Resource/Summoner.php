<?php

namespace Resource;

use Pdo;

class Summoner {

	protected $pdo;

	public function __construct(Pdo $pdo) {
		$this->pdo = $pdo;
	}

	public function get($name) {
		
		$statement = "
			SELECT *
			FROM summoners
			WHERE summoner = :summoner;
		";
		
		$PdoStatement = $this->pdo->prepare($statement);
		$PdoStatement->execute(['summoner' => $name]);

		return $PdoStatement->fetch(Pdo::FETCH_ASSOC);
	
	}

};
