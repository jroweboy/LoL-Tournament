<?php

namespace Resource;

use Pdo;

class Matches {

	protected $pdo;
	protected $queue;
	protected $match;

	public function __construct(Pdo $pdo, Queue $queue, Match $match) {

		$this->pdo = $pdo;
		$this->queue = $queue;
		$this->match = $match;

	}

	public function get($type = 'display', $summoner) {

		$statement = "
			SELECT id
			FROM matches
			WHERE status = :type;";

		$PdoStatement = $this->pdo->prepare($statement);
		$PdoStatement->execute(['type' => $type]);
		$data = $PdoStatement->fetchAll(Pdo::FETCH_ASSOC);

		$matches = [];

		foreach ($data as $match) {
			$matches[$match['id']] = $this->match->get($match['id'], $summoner);
		}

		return $matches;

	}

	public function post($summonerName) {

		$summoners = $this->queue->get();

		foreach ($summoners as &$summoner) {
			$statement = "
				SELECT COUNT(summoner) as count
				FROM matches
				LEFT JOIN teams t ON matches.blue_id = t.id
				LEFT JOIN teams_players tp ON tp.team_id = t.id
				LEFT JOIN summoners s ON tp.summoner_id = s.id
				WHERE s.summoner = :summoner
				ORDER BY count ASC;
			";

			$PdoStatement = $this->pdo->prepare($statement);
			$PdoStatement->execute(['summoner' => $summoner['summoner']]);

			$summoner['played_today'] = $PdoStatement->fetchColumn(0);
		
		}

		$to_play = $this->select($summoners);

		$teams = $this->pickTeams($to_play);

		$teams['match'] = $this->createMatch($teams);

		return $teams;

	}

	

	protected function getMins(array &$summoners) {
		$min = $summoners[0]['played_today'];

		for (
			$min = $summoners['0']['played_today'], $i = 0, $count = count($summoners);
			 $i < $count && $min === $summoners[$i]['played_today'];
			 $i++
		) {}

		$mins = array_splice($summoners, 0, $i);
		

		return $mins;

	}

	protected function select(array $summoners) {
                $to_play = [];

                while (count($to_play) < 10 && count($summoners) > 0) {

                        $mins = $this->getMins($summoners);

                        $index = array_rand($mins);

                        $to_play[] = $mins[$index];

                        array_splice($mins, $index, 1);

                        $summoners = array_merge($mins, $summoners);
                        
                }

		return $to_play;

	}

	protected function winSort($a, $b) {
		return $a['wins'] - $b['wins'];
	}

	protected function pickTeams(array $summoners) {
		$winSort = [$this, 'winSort'];
		usort($summoners, $winSort);

		$teams = [
			'blue' => [],
			'purple' => []
		];

		$blue =& $teams['blue'];
		$purple =& $teams['purple'];

		$blue[] = array_pop($summoners);
		$blue[] = array_shift($summoners);

		$purple[] = array_pop($summoners);
		$purple[] = array_shift($summoners);

		$purple[] = array_pop($summoners);
		$purple[] = array_shift($summoners);

		$blue[] = array_pop($summoners);
		$blue[] = array_pop($summoners);

		$blue[] = array_shift($summoners);
		$purple[] = array_shift($summoners);
		
		usort($blue, $winSort);
		usort($purple, $winSort);

		return $teams;

	}

	protected function createTeam(array $team) {
		$statement = "
			INSERT INTO teams() VALUES();
		";

		$PdoStatement = $this->pdo->prepare($statement);
		$PdoStatement->execute();

	
		$team_id = $this->pdo->lastInsertId();

                $statement = "
                        INSERT INTO teams_players
                               ( summoner_id, team_id)
                        VALUES (:summoner_id, $team_id);
                ";

                $PdoStatement = $this->pdo->prepare($statement);

		foreach ($team as $summoner) {

			$PdoStatement->execute([
				'summoner_id' => $summoner['id']
			]);
		}

		return $team_id;
		
	}

	protected function createMatch(array $teams) {

		$params = [];

		$params['blue_id'] = $this->createTeam($teams['blue']);
		$params['purple_id'] = $this->createTeam($teams['purple']);

		$statement ="
			INSERT INTO matches
			       ( blue_id, purple_id)
			VALUES (:blue_id,:purple_id);
		";

		$PdoStatement = $this->pdo->prepare($statement);
		$PdoStatement->execute($params);

		return $this->pdo->lastInsertId();

	}

};

