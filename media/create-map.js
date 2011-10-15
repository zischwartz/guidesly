
var map;
var markersArray = [];
var geocoder;
var user_location=null;
var user_bound;
var all_markers_bounds;

function show_user_location(position) {
  console.log('got your location!');
  console.log(position);
  var latitude = position.coords.latitude;
  var longitude = position.coords.longitude;
  var accuracy = position.coords.accuracy;
  user_location = new google.maps.LatLng(latitude, longitude);
  map.panTo(user_location);
  map.setZoom(12);

  geocoder.geocode({'latLng': user_location}, function(results, status) {
      if (status == google.maps.GeocoderStatus.OK) {
        if (results[1]) {
			user_bound = results[1].geometry.viewport;
			}
		}
	});//end geocode


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
  geocoder = new google.maps.Geocoder();
  get_location();
  all_markers_bounds = new google.maps.LatLngBounds();
 
  var kansas = new google.maps.LatLng(50.73645526232177, -97.1630858125);
  var mapOptions = {
    zoom: 4,
    center: kansas,
    mapTypeId: google.maps.MapTypeId.ROADMAP,
	streetViewControl: false,
	scrollwheel: false, // ?
  };

  map =  new google.maps.Map(document.getElementById("map_canvas"), mapOptions);

	google.maps.event.addListener(map, 'click', function(event) {
		if (VM.addingPointByHand())
		{	
			addMarker(event.latLng);
			VM.addingPointByHand(0); //take it out of editing mode
		}

		else
			return true;
	});

}

function showAllMarkers()
{
	map.fitBounds(all_markers_bounds);
}

function toggleDraggable() 
{
	if (!VM.draggable())
	{
		$.each(VM.justPlaces() , function(index, element)
		{
			element.make_dragable();
			
		});	
		VM.draggable(1);
	}	
	
	else
	{
		$.each(VM.justPlaces() , function(index, element)
		{
			element.stop_draggable();
		});	
		
		VM.draggable(0);
	}
}


function addMarker(location, address) {
	if (address)
 	{
		var newMapPoint = new anInput({"type":'place', 'lat': location.Ma, 'long': location.Na, 'manual_addy': address});
	 	addInputHelper(newMapPoint);
	}
	else
	{
		var newMapPoint = new anInput({"type":'place', 'lat': location.Ma, 'long': location.Na, });
	 	addInputHelper(newMapPoint);
	}

}



function addAddress() {
	var address= VM.address();
	lookupAddress(function(results){
		map.setCenter(results[0].geometry.location);
		map.setZoom(15);
		addMarker(results[0].geometry.location, address);
	});

}	


function goToAddress()
{
	lookupAddress(function(results){
		map.setCenter(results[0].geometry.location);
	});
}

function lookupAddress(callback) {
	//first check in the user's area
	var address= VM.address();
    geocoder.geocode( { 'address': address, 'bounds': user_bound}, function(results, status) {
      if (status == google.maps.GeocoderStatus.OK) {
		// console.log(results);
		callback(results);

      } 
	///if no dice, search globally
	 else {
			geocoder.geocode( { 'address': address}, function(results, status) {
		      if (status == google.maps.GeocoderStatus.OK) {
			  	callback(results);
				}
			  else
			{
				// still no luck
				VM.mapError("Sorry, we can't find that place. Try adding more info (or less)." )
			} 
				});
		
        // alert("Geocode was not successful for the following reason: " + status);
      } //end else
    });
  } //end lookupaddress




