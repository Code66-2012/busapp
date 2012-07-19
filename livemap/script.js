(function() {
  var fetchBusLocations, processNewJson, updateStops, updateUs;

  $(document).ready(function() {
    var abq, map, mapquest, mapquestUrl, mapquest_attribution, subDomains;
    map = new L.Map('map');
    window.map = map;
    window.markers = {};
    mapquestUrl = 'http://{s}.mqcdn.com/tiles/1.0.0/osm/{z}/{x}/{y}.png';
    subDomains = ['otile1', 'otile2', 'otile3', 'otile4'];
    mapquest_attribution = '<small>Map © <a href="http://openstreetmap.org/">OpenStreetMap</a>, <a href="http://open.mapquest.com">MapQuest</a>; App: <a href="https://github.com/Code66-2012/busapp">Credits & source</a></small>';
    mapquest = new L.TileLayer(mapquestUrl, {
      attribution: mapquest_attribution,
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
    var bus_id, bus_ids_created, bus_ids_deleted, bus_ids_updated, bus_location, bus_marker, item, map, markers, nyanbus, _i, _len;
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
    console.log('Created buses: ' + bus_ids_created.join(','));
    console.log('Updated buses: ' + bus_ids_updated.join(','));
    return console.log('Deleted buses: ' + bus_ids_deleted.join(','));
  };

  updateStops = function(json) {
    var item, m, map, stop_icon, stop_id, stop_ids_created, stop_location, _i, _len, _results;
    map = window.map;
    _results = [];
    for (_i = 0, _len = json.length; _i < _len; _i++) {
      item = json[_i];
      stop_id = item.stopID;
      stop_location = new L.LatLng(parseFloat(item.lat), parseFloat(item.lon));
      stop_ids_created = [];
      stop_icon = L.Icon.extend({
        iconUrl: 'marker-icon-purple.png'
      });
      if (markers['stop' + stop_id] != null) {
        continue;
      } else {
        m = new L.Marker(stop_location, {
          icon: new stop_icon
        });
        m.stop_id = stop_id;
        m.on('click', function(e) {
          var params,
            _this = this;
          params = {
            stop_id: this.stop_id
          };
          return $.ajax({
            url: 'http://blitzforge.com/distance.php',
            dataType: 'json',
            data: params,
            success: function(json) {
              var bus, busItem, html, info, route;
              console.log(json);
              html = "<h2>Stop " + _this.stop_id + "</h2>";
              for (route in json) {
                busItem = json[route];
                html = html + ("<div><h3>Route " + route + "</h3><ul>");
                for (bus in busItem) {
                  info = busItem[bus];
                  html = html + ("<li>Bus " + bus + " in ~" + info.time + " min</li>");
                }
                html = html + "</ul></div>";
              }
              console.log(html);
              return _this.bindPopup(html).openPopup();
            }
          });
        });
        map.addLayer(m);
        markers['stop' + stop_id] = m;
        _results.push(stop_ids_created.push(stop_id));
      }
    }
    return _results;
  };

  updateUs = function(e) {
    var m, markers, me_icon, nyandog_icon, params;
    console.log('Found location ' + e.latlng);
    params = {
      lat: e.latlng.lat,
      lon: e.latlng.lng
    };
    $.ajax({
      url: 'http://blitzforge.com/stops.php',
      dataType: 'json',
      data: params,
      success: updateStops
    });
    markers = window.markers;
    window.map.setView(e.latlng, 16);
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
