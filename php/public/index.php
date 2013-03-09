<?php

use Artax\Http\Request,
    Artax\Http\HeaderBucket,
    Artax\Http\ServerBucket,
    Artax\Http\ParamBucket,
    Artax\Http\Routing\RouteList,
    Artax\Http\Routing\Router,
    Artax\Http\Routing\TokenizerFactory;


/*
 * ------------------------------------------------------------------------
 * Boot Artax.
 * ------------------------------------------------------------------------
 */

define('AX_DEBUG', TRUE);
require '../Artax/Core/Artax-Core.php';


/*
 * ------------------------------------------------------------------------
 * Load event listeners.
 * ------------------------------------------------------------------------
 */

require  '../config/listeners.php';
$artax->pushAll($listeners);


/*
 * ------------------------------------------------------------------------
 * Create a Request; load some Routes; instantiate the Router.
 * ------------------------------------------------------------------------
 */

$request = new Request(new HeaderBucket, new ServerBucket, new ParamBucket);
// Share the Request instance so controllers will be automagically provisioned
// with the same Request object used by the Router. You don't HAVE to do
// this, but it makes sense to avoid forcing the DIC provider to instantiate 
// a new Request object for each class with a Request dependency.
$axDeps->share('Artax\Http\Request', $request);


$routes = new RouteList(new TokenizerFactory);
$routes->addFromFile('../config/routes.txt');


$router = new Router($axDeps, $request, $routes);

/*
 * ------------------------------------------------------------------------
 * Set up application-specific autoloader.
 * ------------------------------------------------------------------------
 */
require '../includes/Autoloader.php';

spl_autoload_register(new Autoloader('../includes'));

/*
 * ------------------------------------------------------------------------
 * Set up application dependencies.
 * ------------------------------------------------------------------------
 */

$pdo = new Pdo(
	'mysql:host=localhost;dbname=lan',
	'monty',
	'python_is_awesome',
	[Pdo::ATTR_ERRMODE => Pdo::ERRMODE_EXCEPTION]
);

$axDeps->share('PDO', $pdo);

/*
 * ------------------------------------------------------------------------
 * Fire up the application.
 * ------------------------------------------------------------------------
 */

session_start();

$_SESSION['summoner'] = 'DotAliscious';

$controllerReturnValue = $router->dispatch();

