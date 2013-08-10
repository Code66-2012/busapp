<?php

mysql_connect('localhost','app','6,$S{1MOL$6_"5lft6');

$stop_id = mysql_real_escape_string($_REQUEST['stop_id']);
$version = $_REQUEST['version'];

date_default_timezone_set('America/Anchorage');

$day = date('w');
$dotw = '';

if($day == 0){
  $dotw = 'sun';
}elseif($day == 6){
  $dotw = 'sat';
}else{
  $dotw = 'wkd';
}

date_default_timezone_set('America/Denver');
if ($version > 2){
$time = date("H:i:s",time()-2400);
}else{
$time = date("H:i:s",time()-120);
}

//if (!is_numeric($stop_id)){
//	$stop_id = 4809;
//}

$sql = "SELECT `arrival_time`,`route`,`trip_id` FROM `abqride`.`trip_map` WHERE `stop_id` = ".$stop_id." AND `active_".$dotw."` = '1' AND `arrival_time` > '".$time."' ORDER BY `arrival_time` ASC LIMIT 10";

$result = mysql_query($sql);

echo mysql_error();
$returned = false;
while ($row = mysql_fetch_array($result)){
	$memcache = new Memcache;
	$memcache->connect('localhost', 11211);
	$seconds_late = $memcache->get($row[2]);
	if ($seconds_late == ""){
		$seconds_late = -1;
	}
	$unix_time = strtotime($row[0]);
	$test_time = (time() - ($unix_time)) - $seconds_late;
	
	if ($test_time < 120){
	
		echo $row[0];
		if ($version > 1){
			echo ";".$row[1];
		}
		if ($version > 2){	
			echo ";".$seconds_late;
		}
		if ($version > 3){
			echo ";".$memcache->get($row[2]."_bus")." ";
		}
		echo "|";
		$returned = true;
	}
}

if (!$returned){
	echo "No More Stops Today";
}	

?>
