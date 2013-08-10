<?php

header('Content-type: application/json');

$memcache = new Memcache;
$memcache->connect('localhost', 11211);

$bus_id = $_REQUEST['bus_id'];

echo $memcache->get("latest");

?>
