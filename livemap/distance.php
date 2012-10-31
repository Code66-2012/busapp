<?php
if ($included != 1){
header('Access-Control-Allow-Origin');
header('Content-type: application/json');
header('Access-Control-Allow-Origin: *');
}

mysql_connect('localhost','root','');
mysql_select_db('abqride');
if (!isset($stop_id)){
	$stop_id = mysql_real_escape_string($_REQUEST['stop_id']);
}
function find_dist($lat,$lon,$new_shape=true){

	global $route_id,$stop_id,$shape_id;
	
	//find nearest point on route shape to bus
	if ($new_shape){
		$sql = "SELECT SQRT(POW(".$lon." - `shape_pt_lon`, 2) + POW(".$lat." - `shape_pt_lat`, 2)) as `distance`, `shape_id`,`shape_pt_sequence` FROM `shapes` WHERE `route_id` = ".$route_id." AND `shape_id` IN (SELECT `shape_id` FROM shape_map WHERE stop_code = ".$stop_id.") ORDER BY `distance` ASC LIMIT 1";
		$dist_find = mysql_query($sql);
		while ($row = mysql_fetch_array($dist_find)){
			
			$shape_id = $row[1];
			//echo "<p>Shape ID:".$shape_id."</p>";
			$bus_sequence = $row[2];
		}
	}else{
		$sql = "SELECT SQRT(POW(".$lon." - `shape_pt_lon`, 2) + POW(".$lat." - `shape_pt_lat`, 2)) as `distance`, `shape_id`,`shape_pt_sequence` FROM `shapes` WHERE `route_id` = ".$route_id." AND `shape_id` = ".$shape_id." ORDER BY `distance` ASC LIMIT 1";
		$dist_find = mysql_query($sql);
		while ($row = mysql_fetch_array($dist_find)){
			//echo "<p>Shape ID:".$shape_id."</p>";
			$bus_sequence = $row[2];
		}
	}
	//find point nearest to stop
	$sql = "SELECT `stop_lat`,`stop_lon` FROM `stops` WHERE `stop_code` = ".$stop_id;
	
	$stop_find = mysql_query($sql);
	while ($row = mysql_fetch_array($stop_find)){
		$lat1 = $row[0];
		$lon1 = $row[1];	
	}
	
	//crow flies distance for now
	//return sqrt(pow($lat-$lat1,2) + pow($lon-$lon1,2));
	//end
	
	$sql = "SELECT SQRT(POW(".$lon1." - `shape_pt_lon`, 2) + POW(".$lat1." - `shape_pt_lat`, 2)) as `distance`, `shape_id`,`shape_pt_sequence` FROM `shapes` WHERE `route_id` = ".$route_id." AND `shape_id` = ".$shape_id." ORDER BY `distance` ASC LIMIT 1";
	$dist_find = mysql_query($sql);
	while ($row = mysql_fetch_array($dist_find)){
		$stop_sequence = $row[2];
	}
	//find difference
	$sql = "SELECT `shape_dist_traveled` FROM  `shapes` WHERE `shape_pt_sequence` = ".$bus_sequence." AND `shape_id` = ".$shape_id;
	$bus_find = mysql_query($sql);
	while ($row = mysql_fetch_array($bus_find)){
		$bus_dist = $row[0];
	}
	$sql = "SELECT `shape_dist_traveled` FROM  `shapes` WHERE `shape_pt_sequence` = ".$stop_sequence." AND `shape_id` = ".$shape_id;
	$stop_find = mysql_query($sql);
	while ($row = mysql_fetch_array($stop_find)){
		$stop_dist = $row[0];
	}
	//echo "SS:".$stop_sequence."BS:".$bus_sequence."    ";
	//echo "SD:".$stop_dist." BD:".$bus_dist;
	$dist = $stop_dist - $bus_dist;
	return $dist;

}


$sql = "SELECT `route_id` FROM  `abqride`.`stops_map` WHERE `stop_code` = ".$stop_id;
$route_find = mysql_query($sql);
if (!$route_find or !mysql_num_rows($route_find)){
	die (json_encode(array("error"=>"Stop Not Found")));
}
while ($row = mysql_fetch_array($route_find)){
	$route_id = $row[0];
	
	$sql = "SELECT `route_short_name` FROM  `abqride`.`routes` WHERE  `route_id` = ".$route_id;
	$routeid_find = mysql_query($sql);
	while ($row = mysql_fetch_array($routeid_find)){
		$route_short_id = $row[0];
	}
	if (!isset($route_short_id)){
		die(json_encode(array("error"=>"Route Not Found")));
	}
	
	//echo "<p>Route ".$route_short_id."</p>";
	
	$sql = "SELECT *,max(id),max(date) FROM code66.locations WHERE routeID = ".$route_short_id." AND date >= DATE_SUB(now(), INTERVAL 370 MINUTE) GROUP BY busID";
	$bus_find = mysql_query($sql);
	$busses = array();
	while ($row = mysql_fetch_array($bus_find)){
		$sql = "SELECT * FROM code66.locations WHERE busID = ".$row['busID']." AND id = ".$row['max(id)']." LIMIT 1";
		$first_find = mysql_query($sql);
		
		if ($row1 = mysql_fetch_array($first_find)){
			$dist = find_dist($row1['lat'],$row1['lon'],true);
			if ($dist < 0){
				continue;
			}
			//echo " 1:".$row1['id'];
		}
		
		$sql = "SELECT * FROM code66.locations WHERE busID = ".$row['busID']." AND id < ".$row['max(id)']." ORDER BY `id` desc LIMIT 1";
		$last_find = mysql_query($sql);
		
		if ($row2 = mysql_fetch_array($last_find)){
			//echo " 2:".$row2['id'];
			$dist2 = find_dist($row2['lat'],$row2['lon'],false);
		}
		
		//echo "D1:".$dist." D2:".$dist2;
		if ((abs($dist) - abs($dist2)) >= 0){
			$dir = "(Traveling Away)";
		}else{
			$dir ="(Traveling Towards)";
			$busses[$row['busID']] = array("distance"=>$dist,"time"=>intval(round($dist*3)));
		}
		
		
		
	}
	
	asort($busses);
	if (count($busses)>0){
		$routes[$route_short_id] = $busses;
	}
	//foreach ($busses as $bus => $dist){
	//	echo "$bus $dist <br/>";
	//}
}

if ($included != 1){
	echo json_encode($routes);
}

?>
