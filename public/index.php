<?php

require_once "../vendor/autoload.php";
require_once "../src/controller/ProjectController.php";

// prepare twig
$loader = new \Twig\Loader\FilesystemLoader('templates');
$twig = new \Twig\Environment($loader, [
	'cache' => 'cache',
]);
  
$pc = new ProjectController();
print_r("<pre>");
print_r($pc->getProjects());
print_r("</pre>");

// Este array lo tiene que devolver el controlador
echo $twig->render('index.html', [ ]);

?>
