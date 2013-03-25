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

<div data-role="page">

	<div data-role="header">
		<h1>All Stops</h1>
	</div><!-- /header -->

	<div data-role="content">
	<ul data-role="listview" data-filter="true">
<?php
mysql_connect('localhost','root','');
if ($_REQUEST['route']){
$sql = 'SELECT * FROM abqride.route_stop_map m,abqride.stops_local s WHERE m.stop_code =s.stop_code AND route = '.mysql_real_escape_string($_REQUEST['route']);
$result = mysql_query($sql);
while ($row = mysql_fetch_array($result)){
echo "<li><a href='stop.php?stop=".$row['stop_code']."&nocache=".time()."'>".$row['stop_name']." ".$row['direction']."</a></li>";
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
