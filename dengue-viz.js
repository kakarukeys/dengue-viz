var map = L.map('map').setView([1.31254, 103.84305], 15),
    data = [
      {coords: [1.32, 103.847], name: "Tan Tock Seng Hospital"},
      {coords: [1.305, 103.845], name: "Istana Park"}
    ];

L.tileLayer('http://{s}.tiles.mapbox.com/v3/kakarukeys.iofn8meo/{z}/{x}/{y}.png', {
  attribution: 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, <a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="http://mapbox.com">Mapbox</a>',
  maxZoom: 18
}).addTo(map);

_.each(data, function(obj) {
  L.marker(obj.coords).addTo(map);
});
