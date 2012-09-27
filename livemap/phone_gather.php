<?php
// page located at http://example.com/process_gather.php
header("content-type: text/xml");
echo "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n";
echo "<Response><Say voice =\"woman\">You entered " . $_REQUEST['Digits']. " .";

mysql_connect('localhost','root','');
mysql_select_db('abqride');
$stop_id = mysql_real_escape_string($_REQUEST['Digits']);
$sql = "SELECT `stop_name` FROM `stops` WHERE `stop_code` = ".$stop_id;
	
	$stop_find = mysql_query($sql);
	if ($row = mysql_fetch_array($stop_find)){
		echo " The Stop Name is ". $row[0].". We do our best to provide accurate information, but please understand that many factors could cause this information to be very inaccurate.";
		$included = 1;
		include ('distance.php');
		$count = 0;
		foreach ($routes as $route_name => $busses){
			foreach ($busses as $bus_id => $info){
				echo " A route ".$route_name." bus is about ".$info['time']." minutes away."; 
				$count ++;
			}
		}
		if ($count == 0){
			echo " No Information for this stop is available at this time, sorry.";
		}
		
		echo " Thank You, Goodbye!";
	
	}else{
		echo "The Stop Was Not Found, Sorry.";
	}

echo "</Say></Response>";
?>