function create_map() {
    var map = L.map('map').setView([1.347833, 103.809357], 11);

    L.tileLayer('http://{s}.tiles.mapbox.com/v3/kakarukeys.iofn8meo/{z}/{x}/{y}.png', {
        attribution: 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, <a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="http://mapbox.com">Mapbox</a>',
        maxZoom: 18
    }).addTo(map);

    return map;
}

function add_clusters(map, markers) {
    var clusters = L.markerClusterGroup();
    clusters.addLayers(markers);
    map.addLayer(clusters);    
}

function create_marker(d) {
    return L.marker(d.coords, {title: d.name});
}

var map = create_map();

$.getJSON("cluster_data.json", function(data) {
    var cases = data.snapshots[0].cases,
        markers = _.map(cases, create_marker);

    add_clusters(map, markers);
});
