<?php

namespace Resource;

use Pdo;

class Match {

	protected $pdo;

	public function __construct(Pdo $pdo) {

		$this->pdo = $pdo;

	}

	public function get($id, $summoner) {

		$statement = "
			SELECT
				s.summoner, 
				s.skype, 
				s.icon, 
				s.wins,
				'blue' AS color,
                                IF(summoner = :summoner, TRUE, FALSE) AS currentUser
			FROM matches m
			LEFT JOIN teams t ON t.id = m.blue_id 
			LEFT JOIN teams_players tp ON t.id = tp.team_id 
			LEFT JOIN summoners s ON s.id = tp.summoner_id
			WHERE m.id = :id

			UNION

                        SELECT
                                s.summoner, 
                                s.skype, 
                                s.icon, 
                                s.wins,
                                'purple' AS color,
                                IF(summoner = :summoner, TRUE, FALSE) AS currentUser
                        FROM matches m
                        LEFT JOIN teams t ON t.id = m.purple_id 
                        LEFT JOIN teams_players tp ON t.id = tp.team_id 
                        LEFT JOIN summoners s ON s.id = tp.summoner_id
                        WHERE m.id = :id
			ORDER BY color ASC, wins DESC

			;";

                $PdoStatement = $this->pdo->prepare($statement);
                $PdoStatement->execute([
			'id' => $id,
			'summoner' => $summoner
		]);
		$PdoStatement->setFetchMode(Pdo::FETCH_ASSOC);

		$data = [
			'match' => $id,
			'blue' => [],
			'purple' => [],
			'skypeGroup' => [],
		];

		$blueGroup = [];
		$purpleGroup = [];

		while ($player = $PdoStatement->fetch()) {

			// There will always be at least 1 result per team
			// because of team color. `summoner` is not allowed to
			// be null.  The only way it can be null is if there
			// was not a result.
			if ($player['summoner'] === NULL) {
				continue;
			}

			$tmp = array_merge([], $player);
			unset($tmp['color']);

			if ($player['color'] == 'blue') {
				if ($player['summoner'] == $summoner) {
					$data['skypeGroup'] =& $blueGroup;
				} else {
					$blueGroup[] = $player['skype'];
				}

				$data['blue'][] = $tmp;


			} else {
				if ($player['summoner'] == $summoner) {
					$data['skypeGroup'] =& $purpleGroup;
				} else {
					$purpleGroup[] = $player['skype'];
				}

				$data['purple'][] = $tmp;

			}

		}

		$this->selectCaptain($data['blue']);
		$this->selectCaptain($data['purple']);

		return $data;

	}

	protected function selectCaptain(array &$team) {
		for ($i = 0, $size = count($team); $i < $size; $i++) {
			if (!empty($team[$i]['skype'])) {
				$team[$i]['captain'] = TRUE;
				break;
			}
		}	

	}

	public function delete($id) {

		$this->pdo->beginTransaction();

		$statement = "
			DELETE
			FROM matches
			WHERE id = :id;
		";

		$PdoStatement = $this->pdo->prepare($statement);
		$PdoStatement->execute(['id' => $id]);

		$statement = "SELECT ROW_COUNT() AS count;";

                $PdoStatement = $this->pdo->query($statement);
		$rowsDeleted = $PdoStatement->fetch(Pdo::FETCH_ASSOC)['count'];

		$this->pdo->rollback();

		return ['rowsDeleted' => $rowsDeleted];
	}

};

