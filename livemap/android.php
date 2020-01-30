<?php

mysql_connect('localhost','app','6,$S{1MOL$6_"5lft6');

$memcache = new Memcache;
$memcache->connect('localhost', 11211);

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

if (strpos($time, "00") === 0) $time = "24"+substr($time, 2);
if (strpos($time, "01") === 0) $time = "25"+substr($time, 2);


//if (!is_numeric($stop_id)){
//	$stop_id = 4809;
//}
if ($version > 4){
$sql_stopid = "";
}else{
$sql_stopid = " OR `stop_id` =".$stop_id;
}

$sql = "SELECT `arrival_time`,`route`,`trip_id` FROM `abqride`.`trip_map` WHERE (`stop_code` = ".$stop_id.$sql_stopid." ) AND `active_".$dotw."` = '1' AND `arrival_time` > '".$time."' ORDER BY `arrival_time` ASC LIMIT 20";

$result = mysql_query($sql);



echo mysql_error();
$returned = false;
while ($row = mysql_fetch_array($result)){
	
	$seconds_late = $memcache->get($row[2]);
	if ($seconds_late == ""){
		$seconds_late = -1;
	}else if ($seconds_late < 0 and $version < 6){
	        //Keeps the app from displaying negative "Minutes Late"
  		$seconds_late = 0;
	} 
	
	if (strpos($row[0], "24") === 0) $row[0] = "00".substr($row[0], 2);
	if (strpos($row[0], "25") === 0) $row[0] = "01".substr($row[0], 2);
			
	$unix_time = strtotime($row[0]);
	$test_time = (time() - ($unix_time)) - $seconds_late;
	//Fix next day issue
	if ($test_time > 21 * 60 * 60){
            $test_time = $test_time - (24 * 60 * 60);
	}
        if ($test_time < -21 * 60 * 60){
            $test_time = $test_time + (24 * 60 * 60);
        }	
	if ($test_time < 120){ //If bus hasn't already passed
	
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
		//if ($test_time > -300 and $seconds_late == -1){
		//	$fp = fopen('missing_data_log.txt', 'a');//opens file in append mode  
		//	fwrite($fp, "Missing Data: stop: $stop_id info:$row[0];$row[1]\n");    
		//	fclose($fp);
		//}
	}
	
}

if (!$returned){
	echo "No More Stops Today";
}	

?>
