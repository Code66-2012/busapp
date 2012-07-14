$(document).ready ->
	map = new L.Map('map')
	window.map = map
	window.currentBusLocations = {}

	mapquestUrl = 'http://{s}.mqcdn.com/tiles/1.0.0/osm/{z}/{x}/{y}.png'
	subDomains = ['otile1','otile2','otile3','otile4']
	mapquestAttrib = 'Data, imagery and map information provided by <a href="http://open.mapquest.co.uk" target="_blank">MapQuest</a>,
	<a href="http://www.openstreetmap.org/" target="_blank">OpenStreetMap</a> and contributors.'
	mapquest = new L.TileLayer(mapquestUrl, {maxZoom: 18, attribution: mapquestAttrib, subdomains: subDomains})

	abq = new L.LatLng(35.08411, -106.65098)
	map.setView(abq, 12)

	map.addLayer(mapquest)

	$.getJSON(
		'http://blitzforge.com/nyan'
		processNewJson
	)

processNewJson = (json) ->
	map = window.map
	for item in json
		bus_location = new L.LatLng(item.coords.lat, item.coords.lon)
		bus_marker = new L.Marker(bus_location)
		map.addLayer(bus_marker)
		
