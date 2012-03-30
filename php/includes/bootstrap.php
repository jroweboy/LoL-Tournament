<?php


$settings = parse_ini_file('lan.conf', true);

require 'rb.php';

R::setup(
    "mysql:host={$settings['mysql']['host']};dbname={$settings['mysql']['db']}", 
    $settings['mysql']['username'], 
    $settings['mysql']['password']
);
R::freeze();