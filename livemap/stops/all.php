<!DOCTYPE html> 
<html>

<head>
	<meta charset="utf-8">
	<meta name="viewport" content="width=device-width, initial-scale=1"> 
	<title>Where's The Bus?, Albuquerque</title> 
	<link rel="stylesheet" href="http://code.jquery.com/mobile/1.2.0/jquery.mobile-1.2.0.min.css" />
	<script src="http://code.jquery.com/jquery-1.8.2.min.js"></script>
	<script src="http://code.jquery.com/mobile/1.2.0/jquery.mobile-1.2.0.min.js"></script>
	
</head> 

<body> 

<div data-role="page">

	<div data-role="header">
		<h1>All Stops</h1>
	</div><!-- /header -->

	<div data-role="content">
	<ul data-role="listview">
<?php
mysql_connect('localhost','root','');
if ($_REQUEST['route']){
$sql = 'SELECT * FROM abqride.route_stop_map m,abqride.stops s WHERE m.stop_code =s.stop_code AND route = '.mysql_real_escape_string($_REQUEST['route']);
$result = mysql_query($sql);
while ($row = mysql_fetch_array($result)){
echo "<li><a data-ajax=\"false\" href='stop.php?stop=".$row['stop_code']."'>".$row['stop_name']."</a></li>";
}
}else{
$result = mysql_query('SELECT * FROM abqride.routes');
while ($row = mysql_fetch_array($result)){
echo "<li><a href='?route=".$row['route_short_name']."'>".$row['route_long_name']." ".$row['route_short_name']."</a></li>";
}
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
