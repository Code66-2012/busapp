$(document).ready ->
	map = new L.Map('map')
	window.map = map
	window.markers = {}

	mapquestUrl = 'http://{s}.mqcdn.com/tiles/1.0.0/osm/{z}/{x}/{y}.png'
	subDomains = ['otile1','otile2','otile3','otile4']
	mapquestAttrib = 'Data, imagery and map information provided by <a href="http://open.mapquest.co.uk" target="_blank">MapQuest</a>,
	<a href="http://www.openstreetmap.org/" target="_blank">OpenStreetMap</a> and contributors.'
	mapquest = new L.TileLayer(mapquestUrl, {maxZoom: 18, subdomains: subDomains})

	abq = new L.LatLng(35.08411, -106.65098)
	map.setView(abq, 12)

	map.addLayer(mapquest)

	map.on('locationfound', updateUs)
	map.locate(watch: true, enableHighAccuracy: true)

	fetchBusLocations()

fetchBusLocations = () ->
	$.getJSON(
		'http://blitzforge.com/nyan'
		processNewJson
	)
	window.setTimeout(fetchBusLocations, 30*1000)

processNewJson = (json) ->
	nyanbus = L.Icon.extend(
		iconUrl: 'nyan-catbus-trans-cropped.gif'
		iconSize: new L.Point(57, 21)
	)

	markers = window.markers

	for item in json
		bus_id = item.bus_id
		bus_location = new L.LatLng(item.coords.lat, item.coords.lon)
		
		if markers[bus_id]?
			console.log 'Updating position for bus ' + bus_id
			markers[bus_id].setLatLng(bus_location)
		else
			console.log 'Creating marker for bus ' + bus_id
			bus_marker = new L.Marker(
				bus_location
			)
			map.addLayer(bus_marker)
			markers[bus_id] = bus_marker

updateUs = (e) ->
	console.log('Found location ' + e.latlng)

	markers = window.markers

	# Recenter zoom and map
	#window.map.setView(e.latlng, 14)

	# If marker has been created already, update position
	if markers['us']?
		m = window.markers['us']
		m.setLatLng(e.latlng)
	# Create marker
	else
		nyandog_icon = L.Icon.extend(
			iconUrl: 'nyan-dog.png'
			iconSize: new L.Point(77, 22)
		)
		me_icon = L.Icon.extend(
			iconUrl: 'marker-icon-red.png'
		)
		m = new L.Marker(
			e.latlng
			icon: new me_icon
		)
		map.addLayer(m)
		markers['us'] = m
