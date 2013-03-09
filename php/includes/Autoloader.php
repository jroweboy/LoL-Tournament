<?php

class Autoloader {

	protected $root;

	public function __construct($root = __DIR__) {
		$this->root = $root;
	}

	public function canLoad($class) {
		$class = str_replace('\\', '/', $class);
		return file_exists($this->root . "/$class.php");
	}

	public function load($class) {
		$class = str_replace('\\', '/', $class);
		if (!$this->canLoad($class)) {
			echo "Couldn't load";
			return;
		}

		require $this->root . "/$class.php";

	}

	public function __invoke($class) {
		$this->load($class);
	}

}

