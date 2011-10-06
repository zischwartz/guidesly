
var map;
var markersArray = [];
var geocoder;
var user_location=null;
var user_region=null;

function show_user_location(position) {
  console.log('got your location!');
  console.log(position);
  var latitude = position.coords.latitude;
  var longitude = position.coords.longitude;
  var accuracy = position.coords.accuracy;
  user_location = new google.maps.LatLng(latitude, longitude);
  map.panTo(user_location);
  map.setZoom(12);
  if (position.address)
	if (position.address.region)
		{
			user_region= position.address.region;
			console.log(user_region);
			// document.getElementById("region").setValue(position.address.region);
		}
  // console.log(accuracy);

}



function get_location() {
  // if (Modernizr.geolocation) {
	// console.log('getting it');
    navigator.geolocation.getCurrentPosition(show_user_location);
  // } else {
	
    // no native support; maybe try Gears?
  // }
}



function initialize_map() {
  get_location();
	
  geocoder = new google.maps.Geocoder();
	
  var kansas = new google.maps.LatLng(50.73645526232177, -97.1630858125);
  var mapOptions = {
    zoom: 4,
    center: kansas,
    mapTypeId: google.maps.MapTypeId.TERRAIN
  };

  map =  new google.maps.Map(document.getElementById("map_canvas"), mapOptions);

//make this a state  
google.maps.event.addListener(map, 'click', function(event) {
    addMarker(event.latLng);
  });

}




function addMarker(location) {
	var infowindow = new google.maps.InfoWindow({
	    content: 'Hello this is some content'
	});
	
  marker = new google.maps.Marker({
    position: location,
    map: map,
    animation: google.maps.Animation.DROP,
	title:"Hello World!"
  });
										//'mouseover'
	google.maps.event.addListener(marker, 'click', function() {
	  infowindow.open(map,marker);
	});
	
  markersArray.push(marker);
}





// Removes the overlays from the map, but keeps them in the array
function clearOverlays() {
  if (markersArray) {
    for (i in markersArray) {
      markersArray[i].setMap(null);
    }
  }
}

// Shows any overlays currently in the array
function showOverlays() {
  if (markersArray) {
    for (i in markersArray) {
      markersArray[i].setMap(map);
    }
  }
}

// Deletes all markers in the array by removing references to them
function deleteOverlays() {
  if (markersArray) {
    for (i in markersArray) {
      markersArray[i].setMap(null);
    }
    markersArray.length = 0;
  }
}


function codeAddress() {
    var address = document.getElementById("address").value;
	var region = user_region;
	address += region;
    geocoder.geocode( { 'address': address}, function(results, status) {
      if (status == google.maps.GeocoderStatus.OK) {
		console.log(results);
        map.setCenter(results[0].geometry.location);
		map.setZoom(15);
		addMarker(results[0].geometry.location);
        // var marker = new google.maps.Marker({
        //     map: map,
        //     position: results[0].geometry.location
        // });
      } else {
        alert("Geocode was not successful for the following reason: " + status);
      }
    });
  }




















// 
// var map;
// var $latlng;
// var overlay;
// var markersArray = [];
// var geocoder = new google.maps.Geocoder();
// 
// 
//             
// function initialize() {            
//      
//  var myLatlng = new google.maps.LatLng(40.715, -74.002);
//  var myOptions = {
//     zoom: 10,
//     center: myLatlng,
//     mapTypeId: google.maps.MapTypeId.ROADMAP
//   }
//   
//   
// map = new google.maps.Map(document.getElementById("map_canvas"),
//     myOptions);
// 
//   google.maps.event.addListener(map, 'click', function(event) {
//     placeMarker(event.latLng);
//  	}); 
//  }
// 
// 
// 
// function placeMarker(location) {
//   var clickedLocation = new google.maps.LatLng(location);
//   var marker = new google.maps.Marker({
//       position: location, 
//       map: map,
//       draggable: true 
//       });
//       
//       
//   VM.addPoint2Map(location); // Post point to server (card.js)
//   markersArray.push(marker); // Put marker in array with rest of markers
//   
//   geocodePosition(marker.getPosition());
//   google.maps.event.addListener(marker, 'drag', function() {
//     updateMarkerPosition(marker.getPosition());
//   	});
//   google.maps.event.addListener(marker, 'dragend', function() {
//     geocodePosition(marker.getPosition());
//   	});
//   google.maps.event.addListener(marker, 'click', function() {
//     alert('Point clicked');
//     });
// }

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
      


