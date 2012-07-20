$(document).ready ->
	map = new L.Map('map')
	window.map = map
	window.markers = {}

	mapquestUrl = 'http://{s}.mqcdn.com/tiles/1.0.0/osm/{z}/{x}/{y}.png'
	subDomains = ['otile1','otile2','otile3','otile4']
	mapquest_attribution = '<small>Map © <a href="http://openstreetmap.org/">OpenStreetMap</a>, <a href="http://open.mapquest.com">MapQuest</a>; App: <a href="https://github.com/Code66-2012/busapp">Credits & source</a></small>'
	mapquest = new L.TileLayer(mapquestUrl, {attribution: mapquest_attribution, maxZoom: 18, subdomains: subDomains})

	abq = new L.LatLng(35.08411, -106.65098)
	map.setView(abq, 12)

	map.addLayer(mapquest)

	# Fix marker animation on zoom
	map.on 'zoomstart', (e) ->
		$('body').addClass('zoom-in-progress')
	map.on 'zoomend', (e) ->
		$('body').removeClass('zoom-in-progress')

	map.on('locationfound', updateUs)
	map.locate(watch: true, enableHighAccuracy: true)

	fetchBusLocations()

################################################################################

fetchBusLocations = () ->
	$.getJSON(
		'http://blitzforge.com/rt'
		processNewJson
	)
	window.setTimeout(fetchBusLocations, 30*1000)

################################################################################

processNewJson = (json) ->
	nyanbus = L.Icon.extend(
		iconUrl: 'nyan-catbus-trans-cropped.gif'
		iconSize: new L.Point(57, 21)
	)

	markers = window.markers
	map = window.map

	bus_ids_created = []
	bus_ids_updated = []
	bus_ids_deleted = []

	for item in json
		bus_id = item.bus_id
		bus_location = new L.LatLng(item.coords.lat, item.coords.lon)
		
		# Update position of bus
		if markers[bus_id]?
			bus_ids_updated.push(bus_id)
			markers[bus_id].setLatLng(bus_location)
		# Create markers for new bus
		else
			bus_ids_created.push(bus_id)
			bus_marker = new L.Marker(
				bus_location
			)
			map.addLayer(bus_marker)
			markers[bus_id] = bus_marker

	# Remove buses we are no longer tracking
#	for bus_id, marker of markers
#		if bus_id in bus_ids_updated or bus_id in bus_ids_created
#			continue
#
#		map.removeLayer(marker)
#		delete markers[bus_id]
#		bus_ids_deleted.push(bus_id)

	console.log 'Created buses: ' + bus_ids_created.join(',')
	console.log 'Updated buses: ' + bus_ids_updated.join(',')
	console.log 'Deleted buses: ' + bus_ids_deleted.join(',')

################################################################################

updateStops = (json) ->
	map = window.map

	for item in json
		stop_id = item.stopID
		stop_location = new L.LatLng(parseFloat(item.lat), parseFloat(item.lon))
		stop_ids_created = []

		stop_icon = L.Icon.extend(
			iconUrl: 'marker-icon-purple.png'
		)

		# If the stop is already on the map, ignore
		if markers['stop' + stop_id]?
			continue

		# Stop is not on the map
		else
			m = new L.Marker(
				stop_location
				icon: new stop_icon
			)

			m.stop_id = stop_id

			m.on 'click', (e) ->
				params = stop_id: this.stop_id
				$.ajax(
					url: 'http://blitzforge.com/distance.php'
					dataType: 'json'
					data: params
					success: (json) =>
						console.log json
						html = "<h2>Stop #{ this.stop_id }</h2>"
						for route, busItem of json
							html = html + "<div><h3>Route #{ route }</h3><ul>"
							for bus, info of busItem
								html = html + "<li>Bus #{ bus } in ~#{ info.time } min</li>"
							html = html + "</ul></div>"

						console.log html
							
						this.bindPopup(html).openPopup()
#					error: (json) =>
#							html = "<div><h3>No buses for route #{ this.stop_id } today</h3><ul>"
#
#						console.log html
#							
#						this.bindPopup(html).openPopup()
				)
						
			map.addLayer(m)
			markers['stop' + stop_id] = m
			stop_ids_created.push	stop_id

################################################################################

updateUs = (e) ->
	console.log('Found location ' + e.latlng)

	# Fetch closest stops
	params = lat: e.latlng.lat, lon: e.latlng.lng
	$.ajax(
		url: 'http://blitzforge.com/stops.php'
		dataType: 'json'
		data : params
		success: updateStops
	)

	markers = window.markers

	# Recenter zoom and map
	window.map.setView(e.latlng, 16)

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
