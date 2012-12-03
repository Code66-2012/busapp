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
		<h1>Nearest Stops</h1>
	</div><!-- /header -->

	<div data-role="content">
		
			<div id="div-stops">
			</div>
		
	
	</div><!-- /content -->
	
	<div data-role="footer">
		<h4>Albuquerque</h4>
	</div><!-- /footer -->
	
	<script>
	if (navigator.geolocation) {
         navigator.geolocation.getCurrentPosition(onSuccess, onError);
    } else {
         // If location is not supported on this platform, disable it
         alert("You're device doesn't support Geolocation here.");
    }
	
	function onSuccess(position)
	{
    $.getJSON("http://speedycomputing.net/nextbus/stops.php?lat="+position.coords.latitude+"&lon="+position.coords.longitude, function(data) {
		//alert(data);
		var html = "<ul data-role=\"listview\">";
        $.each(data, function(i, item) {
            html += '<li><a href="stop.php?stop=' + item.id +'&nocache='+Math.round((new Date()).getTime() / 10000)+'">' + item.name;
			for (var i=0;i<item.routes.length;i++)
			{
				html += "["+item.routes[i]+"]";
			}
			html += "("+item.dir+")</a></li>";
        });
		//html += "<li><a href=\"#\">Load More</a></li></ul>";
		$(html).appendTo("#div-stops").listview();
    });

	}
 
// Error function for Geolocation call
	function onError(msg)
	{
     alert(msg);
	}
	</script>
	
</div><!-- /page -->
	
</body>
</html>
