
var map;
var $latlng;
var overlay;
var markersArray = [];
var geocoder = new google.maps.Geocoder();


            
function initialize() {            
     
 var myLatlng = new google.maps.LatLng(40.715, -74.002);
 var myOptions = {
    zoom: 10,
    center: myLatlng,
    mapTypeId: google.maps.MapTypeId.ROADMAP
  }
  
  
map = new google.maps.Map(document.getElementById("map_canvas"),
    myOptions);

  google.maps.event.addListener(map, 'click', function(event) {
    placeMarker(event.latLng);
 	}); 
 }



function placeMarker(location) {
  var clickedLocation = new google.maps.LatLng(location);
  var marker = new google.maps.Marker({
      position: location, 
      map: map,
      draggable: true 
      });
      
      
  VM.addPoint2Map(location); // Post point to server (card.js)
  markersArray.push(marker); // Put marker in array with rest of markers
  
  geocodePosition(marker.getPosition());
  google.maps.event.addListener(marker, 'drag', function() {
    updateMarkerPosition(marker.getPosition());
  	});
  google.maps.event.addListener(marker, 'dragend', function() {
    geocodePosition(marker.getPosition());
  	});
  google.maps.event.addListener(marker, 'click', function() {
    alert('Point clicked');
    });
}

/*
function deleteMarker(location) {
  if (markersArray) {
    for (i in markersArray) {
   	  if (markersArray[i].getPosition() == location) {
        markersArray[i].setMap(null);
        markersArray.splice(i,1);
      }
    }
  }
}

function geocodePosition(pos) {
  geocoder.geocode({
    latLng: pos
  }, function(responses) {
    if (responses && responses.length > 0) {
      updateMarkerAddress(responses[0].formatted_address);
    } else {
      updateMarkerAddress('Cannot determine address at this location.');
    }
  });
}

 
function updateMarkerAddress(str) {
 // document.getElementById('address_div').innerHTML = str;
}

function manualAddress() {
  var address = document.getElementById("address").value;
  geocoder.geocode( { 'address': address}, function(results, status) {
    if (status == google.maps.GeocoderStatus.OK) {
      map.setCenter(results[0].geometry.location);
      placeMarker(results[0].geometry.location);
    } else {
      alert("Geocode was not successful for the following reason: " + status);
    }
  });
}
*/
      


