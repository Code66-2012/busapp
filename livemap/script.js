(function() {
  var fetchBusLocations, processNewJson, updateUs,
    __indexOf = Array.prototype.indexOf || function(item) { for (var i = 0, l = this.length; i < l; i++) { if (i in this && this[i] === item) return i; } return -1; };

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
      subdomains: subDomains
    });
    abq = new L.LatLng(35.08411, -106.65098);
    map.setView(abq, 12);
    map.addLayer(mapquest);
    map.on('zoomstart', function(e) {
      return $('body').addClass('zoom-in-progress');
    });
    map.on('zoomend', function(e) {
      return $('body').removeClass('zoom-in-progress');
    });
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
    var bus_id, bus_ids_created, bus_ids_deleted, bus_ids_updated, bus_location, bus_marker, item, map, marker, markers, nyanbus, _i, _len;
    nyanbus = L.Icon.extend({
      iconUrl: 'nyan-catbus-trans-cropped.gif',
      iconSize: new L.Point(57, 21)
    });
    markers = window.markers;
    map = window.map;
    bus_ids_created = [];
    bus_ids_updated = [];
    bus_ids_deleted = [];
    for (_i = 0, _len = json.length; _i < _len; _i++) {
      item = json[_i];
      bus_id = item.bus_id;
      bus_location = new L.LatLng(item.coords.lat, item.coords.lon);
      if (markers[bus_id] != null) {
        bus_ids_updated.push(bus_id);
        markers[bus_id].setLatLng(bus_location);
      } else {
        bus_ids_created.push(bus_id);
        bus_marker = new L.Marker(bus_location);
        map.addLayer(bus_marker);
        markers[bus_id] = bus_marker;
      }
    }
    for (bus_id in markers) {
      marker = markers[bus_id];
      if (__indexOf.call(bus_ids_updated, bus_id) >= 0 || __indexOf.call(bus_ids_created, bus_id) >= 0) {
        continue;
      }
      map.removeLayer(marker);
      delete markers[bus_id];
      bus_ids_deleted.push(bus_id);
    }
    console.log('Created buses: ' + bus_ids_created.join(','));
    console.log('Updated buses: ' + bus_ids_updated.join(','));
    return console.log('Deleted buses: ' + bus_ids_deleted.join(','));
  };

  updateUs = function(e) {
    var m, markers, me_icon, nyandog_icon;
    console.log('Found location ' + e.latlng);
    markers = window.markers;
    if (markers['us'] != null) {
      m = window.markers['us'];
      return m.setLatLng(e.latlng);
    } else {
      nyandog_icon = L.Icon.extend({
        iconUrl: 'nyan-dog.png',
        iconSize: new L.Point(77, 22)
      });
      me_icon = L.Icon.extend({
        iconUrl: 'marker-icon-red.png'
      });
      m = new L.Marker(e.latlng, {
        icon: new me_icon
      });
      map.addLayer(m);
      return markers['us'] = m;
    }
  };

}).call(this);
