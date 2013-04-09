<?php

$return = array();

if ($_GET['lat'] && $_GET['lon']) {
	header('Access-Control-Allow-Origin:*');
	header('Content-type: application/json');
	header('Access-Control-Allow-Origin: *');
	//$sql = new mysqli('localhost', 'dev', 'root', 'code66');
	mysql_connect('localhost', 'root', '');
	mysql_select_db('code66');

	$lat = floatval($_GET['lat']);
	$lat_ceil = $lat + .006;
	$lat_floor = $lat - .006;
	$lon = floatval($_GET['lon']);
	$lon_ceil = $lon + .006;
	$lon_floor = $lon - .006;

	$query = sprintf("SELECT * FROM stops WHERE (lat < %F && lat > %F) && (lon < %F && lon > %F)", $lat_ceil, $lat_floor, $lon_ceil, $lon_floor);

	$result = mysql_query($query) or die(mysql_error());
	while ($stop = mysql_fetch_assoc($result)) {
		$return[] = $stop;
	}
}

echo json_encode($return);
