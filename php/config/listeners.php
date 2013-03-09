<?php

use Artax\Http\Request;
use Artax\Http\Exceptions\NotFoundException;
use Artax\Http\Exceptions\MethodNotAllowedException;
use Artax\Http\Exceptions\HttpException;

$listeners = new StdClass;

/*
 * ------------------------------------------------------------------------
 * Specify routing error listeners
 * 
 * `Router::dispatch()` will throw a NotFoundException if no Route is found
 * to match the request URI. Alternatively, if a route match is found but the
 * corresponding class controller doesn't expose a public method matching the
 * HTTP request verb, a MethodNotAllowedException is thrown. It's up to you
 * to do something appropriate with these uncaught exceptions in your
 * `exception` event listener(s)
 * ------------------------------------------------------------------------
 */


$listeners->error = function(ErrorException $e, $debug) {

    $code = $e->getCode();
    if (!$debug && ($code == E_STRICT || $code == E_DEPRECATED)) {
        // do some logging or just ignore in production
    } else {
        throw $e;
    }
};

$listeners->exception = function(Exception $e, $debug) {
    
    if ($e instanceof NotFoundException) {
	header('HTTP/1.1 404 Not Found');
    } elseif ($e instanceof MethodNotAllowedException) {
	header('HTTP/1.1 405 Method Not Allowed');
    } elseif ($e instanceof HttpException) {
        header("HTTP/1.1. {$e->getCode()} {$e->getMessage()}");
    } else {
	header('HTTP/1.1 500 Internal Server Error');
        echo PHP_EOL . '500 Internal Server Error' . PHP_EOL . PHP_EOL;
        echo $debug ? $e : 'Oops, we had a problem!';
        echo PHP_EOL;
    }
};
