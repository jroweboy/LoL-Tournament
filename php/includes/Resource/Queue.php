<?php

namespace Resource;

use Pdo;

class Queue {

	protected $pdo;

	public function __construct(Pdo $pdo) {
		$this->pdo = $pdo;
	}

	public function get() {

		$statement = "
			SELECT * 
			FROM summoners
			WHERE in_queue;
		";

		$PdoStatement = $this->pdo->prepare($statement);
		$PdoStatement->execute();
		$summoners = $PdoStatement->fetchAll(Pdo::FETCH_ASSOC);

		return $summoners;
	}

	public function post($in_queue, $summoner) {
		$statement = "
			UPDATE summoners
			SET in_queue = :in_queue
			WHERE summoner = :summoner;
		";

		$PdoStatement = $this->pdo->prepare($statement);
		$PdoStatement->execute([
			'in_queue' => filter_var($in_queue, FILTER_VALIDATE_BOOLEAN) == true ? 1 : 0,
			'summoner' => $summoner,
		]);

		return $this->get();

	}

};

