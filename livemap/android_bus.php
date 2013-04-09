<?php

$memcache = new Memcache;
$memcache->connect('localhost', 11211);

$bus_id = $_REQUEST['bus_id'];

echo $memcache->get($bus_id."_ns").":".$memcache->get($bus_id."_coords");

?>
