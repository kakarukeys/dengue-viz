function create_map() {
    var map = L.map('map').setView([1.36, 103.809357], 12);

    L.tileLayer('http://{s}.tiles.mapbox.com/v3/kakarukeys.iofn8meo/{z}/{x}/{y}.png', {
        attribution: 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, <a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="http://mapbox.com">Mapbox</a>',
        maxZoom: 18
    }).addTo(map);

    return map;
}

function create_marker(d) {
    return L.marker(d.coords, {title: d.name});
}

function process_cluster_data(cluster_data) {
    var cases = cluster_data.snapshots[0].cases;
    return _.map(cases, create_marker);
}

function process_marker_data(marker_data) {
    var sites = marker_data.groups[0].sites;

    return _.map(sites, function(d) {
        return create_marker(d).bindPopup("<b>"+d.name+"</b>");
    });
}

function create_cluster_layer(markers) {
    return L.markerClusterGroup().addLayers(markers);
}

function create_marker_layer(markers) {
    return L.layerGroup(markers);
}

var cluster_layer = $.getJSON("cluster_data.json")
        .then(process_cluster_data)
        .then(create_cluster_layer),

    marker_layer = $.getJSON("marker_data.json")
        .then(process_marker_data)
        .then(create_marker_layer),

    map = create_map();

function add_layer(layer) {
    map.addLayer(layer);
}

cluster_layer.done(add_layer);
marker_layer.done(add_layer);
