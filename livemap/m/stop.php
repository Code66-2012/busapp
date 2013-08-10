<?php
header("Cache-Control: no-cache, no-store, must-revalidate");
header("Expires: -1");
?>

<!DOCTYPE html> 
<html>

<head>
	<meta charset="utf-8">
	<meta name="viewport" content="width=device-width, initial-scale=1"> 
	<title>Where's The Bus?, Albuquerque</title> 
	<link rel="stylesheet" href="http://code.jquery.com/mobile/1.2.0/jquery.mobile-1.2.0.min.css" />
	<script src="http://code.jquery.com/jquery-1.8.2.min.js"></script>
	<script src="http://code.jquery.com/mobile/1.2.0/jquery.mobile-1.2.0.min.js"></script>
		<script type="text/javascript">

	  var _gaq = _gaq || [];
	  _gaq.push(['_setAccount', 'UA-410552-12']);
	  _gaq.push(['_trackPageview']);

	  (function() {
		var ga = document.createElement('script'); ga.type = 'text/javascript'; ga.async = true;
		ga.src = ('https:' == document.location.protocol ? 'https://ssl' : 'http://www') + '.google-analytics.com/ga.js';
		var s = document.getElementsByTagName('script')[0]; s.parentNode.insertBefore(ga, s);
	  })();

	</script>
	</head> 

<body> 

<div data-role="page" data-dom-cache="false">

	<div data-role="header">
		<h1>Bus Stop</h1>
	</div><!-- /header -->

	<div data-role="content">	
<ul data-role="listview">
<?php

error_reporting(E_ALL);
ini_set('display_errors', '1');

mysql_connect('localhost','app','6,$S{1MOL$6_"5lft6');
$stop_id = mysql_real_escape_string($_REQUEST['stop']);



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

$time = date("H:i:s",time()-1200);

//if (!is_numeric($stop_id)){
//	$stop_id = 4809;
//}

$sql = "SELECT `arrival_time`,`route`,`trip_id` FROM `abqride`.`trip_map` WHERE `stop_code` = ".$stop_id." AND `active_".$dotw."` = 1 AND `arrival_time` > '".$time."' ORDER BY `arrival_time` ASC LIMIT 20";

$result = mysql_query($sql);

echo mysql_error();

$memcache = new Memcache;
$memcache->connect('localhost', 11211);

while ($row = mysql_fetch_array($result)){
	$seconds_late = $memcache->get($row[2]);
	$real_time = "";
	$unix_time = strtotime($row[0]);
	$test_time = time() - ($unix_time);  //A measure of the time since the bus should have come (negative means it should still be coming)
	if (is_numeric($seconds_late)){
		if ($seconds_late == 0){
			$real_time = "<b style='color:green;'>On Time</b>";
		}else{
			$test_time -= $seconds_late;
			$minutes_late = ceil($seconds_late/60);
			if ($minutes_late == 1){
				$real_time = "<b style='color:#CC3300'>1 minute late</b>";
			}else{
				$real_time = "<b style='color:red'>".$minutes_late." minutes late</b>";
			}
		}
	}
	if ($test_time < 120){
		echo "<li test_time = '".$test_time."'>Rt ".$row[1].": Scheduled ".date('g:i a', $unix_time)." ".$real_time."</li>";
	}
}

if (mysql_num_rows($result) == 0){
	echo "<li>No More Stops Today</li>";
}	

?>
</ul>
	</div><!-- /content -->
	
	<div data-role="footer">
		<h4>Albuquerque</h4>
	</div><!-- /footer -->
	
</div><!-- /page -->

</body>
</html>
