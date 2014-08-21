function create_map() {
    var map = L.map('map').setView([1.347833, 103.809357], 11);

    L.tileLayer('http://{s}.tiles.mapbox.com/v3/kakarukeys.iofn8meo/{z}/{x}/{y}.png', {
        attribution: 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, <a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="http://mapbox.com">Mapbox</a>',
        maxZoom: 18
    }).addTo(map);

    return map;
}

function create_marker(d) {
    return L.marker(d.coords, {title: d.name});
}

function process_data(cluster_data) {
    var cases = cluster_data.snapshots[0].cases;
    return _.map(cases, create_marker);
}

function create_clusters(markers) {
    return L.markerClusterGroup().addLayers(markers);
}
function add_markers(){
	$.getJSON("marker_data.json", function(data){
	
	for (var i = 0; i < data.length; i++) {
			marker = new L.marker([data[i].coords[0],data[i].coords[1]])
				.bindPopup("<b>"+data[i].name+"</b><br><b>Cases : </b>"+data[i].total )
				.addTo(map)
		}
 });
}
add_markers();
var promise = $.getJSON("cluster_data.json")
        .then(process_data)
        .then(create_clusters),


    map = create_map();
	
promise.done(function(clusters) {
    map.addLayer(clusters);
});    
