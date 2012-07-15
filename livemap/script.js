(function() {
  var fetchBusLocations, processNewJson, updateUs;

  $(document).ready(function() {
    var abq, map, mapquest, mapquestAttrib, mapquestUrl, subDomains;
    map = new L.Map('map');
    window.map = map;
    window.markers = {};
    mapquestUrl = 'http://{s}.mqcdn.com/tiles/1.0.0/osm/{z}/{x}/{y}.png';
    subDomains = ['otile1', 'otile2', 'otile3', 'otile4'];
    mapquestAttrib = 'Data, imagery and map information provided by <a href="http://open.mapquest.co.uk" target="_blank">MapQuest</a>,\
	<a href="http://www.openstreetmap.org/" target="_blank">OpenStreetMap</a> and contributors.';
    mapquest = new L.TileLayer(mapquestUrl, {
      maxZoom: 18,
      attribution: mapquestAttrib,
      subdomains: subDomains
    });
    abq = new L.LatLng(35.08411, -106.65098);
    map.setView(abq, 12);
    map.addLayer(mapquest);
    map.on('locationfound', updateUs);
    map.locate({
      watch: true,
      enableHighAccuracy: true
    });
    return fetchBusLocations();
  });

  fetchBusLocations = function() {
    $.getJSON('http://blitzforge.com/nyan', processNewJson);
    return window.setTimeout(fetchBusLocations, 30 * 1000);
  };

  processNewJson = function(json) {
    var bus_id, bus_location, bus_marker, item, markers, nyanbus, _i, _len, _results;
    markers = window.markers;
    _results = [];
    for (_i = 0, _len = json.length; _i < _len; _i++) {
      item = json[_i];
      bus_id = item.bus_id;
      bus_location = new L.LatLng(item.coords.lat, item.coords.lon);
      nyanbus = L.Icon.extend({
        iconUrl: 'nyan-catbus-trans-cropped.gif',
        iconSize: new L.Point(57, 21)
      });
      if (markers[bus_id] != null) {
        console.log('Updating position for bus' + bus_id);
        _results.push(markers[bus_id].setLatLng(bus_location));
      } else {
        console.log('Creating marker for bus' + bus_id);
        bus_marker = new L.Marker(bus_location);
        map.addLayer(bus_marker);
        _results.push(markers[bus_id] = bus_marker);
      }
    }
    return _results;
  };

  updateUs = function(e) {
    var marker, markers, me_icon, nyandog;
    console.log('Found location ' + e.latlng);
    markers = window.markers;
    if (markers['us'] != null) {
      marker = window.markers.us;
      return marker.setLatLng(e.latlng);
    } else {
      nyandog = L.Icon.extend({
        iconUrl: 'nyan-dog.png',
        iconSize: new L.Point(77, 22)
      });
      me_icon = L.Icon.extend({
        iconUrl: 'marker-icon-red.png'
      });
      marker = new L.Marker(e.latlng, {
        icon: new me_icon
      });
      map.addLayer(marker);
      return markers['us'] = nyandog;
    }
  };

}).call(this);
