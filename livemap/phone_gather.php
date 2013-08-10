<?php
// page located at http://example.com/process_gather.php
header("content-type: text/xml");
echo "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n";
echo "<Response><Say voice =\"woman\">You entered " . $_REQUEST['Digits']. " .";

mysql_connect('localhost','app','6,$S{1MOL$6_"5lft6');
mysql_select_db('abqride');
$stop_id = mysql_real_escape_string($_REQUEST['Digits']);
$sql = "SELECT `stop_name` FROM `stops` WHERE `stop_code` = ".$stop_id;
	
	$stop_find = mysql_query($sql);
	if ($row = mysql_fetch_array($stop_find)){
		echo " The Stop Name is ". $row[0].".";

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

		$sql = "SELECT `arrival_time`,`route`,`trip_id` FROM `abqride`.`trip_map` WHERE `stop_id` = ".$stop_id." AND `active_".$dotw."` = '1' AND `arrival_time` > '".$time."' ORDER BY `arrival_time` ASC LIMIT 5";

		$result = mysql_query($sql);
		$memcache = new Memcache;
		$memcache->connect('localhost', 11211);
		while ($row = mysql_fetch_array($result)){
			
			$seconds_late = $memcache->get($row[2]);
			$unix_time = strtotime($row[0]);
			echo " There is a route ".$row[1]." bus scheduled to arrive at ".date('g:i', $unix_time).".";
			if ($seconds_late != ""){
				if ($seconds_late < 90){
					echo " It is estimated to arrive on time.";
				}else{
					echo " It is estimated to arrive ".floor($seconds_late/60)." minutes late.";
				}
			}
			
		}

		if (mysql_num_rows($result) == 0){
			echo " No More Stops are scheduled Today.";
		}
		echo " The information is updated every minute. To help keep this service free, please wait at least a full minute to call again. Thank You! Goodbye.</Say>";
	}else{
		echo '</Say><Gather timeout="10" action="/phone_gather.php" method="GET"><Say voice = "woman">The Stop Was Not Found, Try Again.</Say></Gather>';
	}

echo "</Response>";
?>
