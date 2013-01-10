<?php

$stop_id = mysql_real_escape_string($_REQUEST['stop_id']);
$version = $_REQUEST['version'];
mysql_connect('localhost','root','');

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

$time = date("H:i:s",time()-120);

//if (!is_numeric($stop_id)){
//	$stop_id = 4809;
//}

$sql = "SELECT `arrival_time`,`route`,`trip_id` FROM `abqride`.`trip_map` WHERE `stop_id` = ".$stop_id." AND `active_".$dotw."` = '1' AND `arrival_time` > '".$time."' ORDER BY `arrival_time` ASC LIMIT 10";

$result = mysql_query($sql);

echo mysql_error();

while ($row = mysql_fetch_array($result)){
	echo $row[0];
	if ($version > 1){
		echo ";".$row[1];
	}
	if ($version > 2){
		$memcache = new Memcache;
		$memcache->connect('localhost', 11211);
		$seconds_late = $memcache->get($row[2]);
		if ($seconds_late == ""){
			$seconds_late = -1;
		}
		echo ";".$seconds_late;
    }
	echo "|";
}

if (mysql_num_rows($result) == 0){
	echo "No More Stops Today";
}	

?>
