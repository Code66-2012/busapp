(function() {
  var processNewJson;

  $(document).ready(function() {
    var abq, map, mapquest, mapquestAttrib, mapquestUrl, subDomains;
    map = new L.Map('map');
    window.map = map;
    window.currentBusLocations = {};
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
    return $.getJSON('http://blitzforge.com/nyan', processNewJson);
  });

  processNewJson = function(json) {
    var bus_location, bus_marker, item, map, _i, _len, _results;
    map = window.map;
    _results = [];
    for (_i = 0, _len = json.length; _i < _len; _i++) {
      item = json[_i];
      bus_location = new L.LatLng(item.coords.lat, item.coords.lon);
      bus_marker = new L.Marker(bus_location);
      _results.push(map.addLayer(bus_marker));
    }
    return _results;
  };

}).call(this);
