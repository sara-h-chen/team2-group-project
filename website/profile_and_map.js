function getMessages(ID, init){
	contact=ID;
  $("#messages").empty();
	$("#message_header").empty();
	if (init){
		$("#message_view").toggle();
	}
	url = 'http://localhost:8000/backend/function/'+ID+'/';
	$.get(url, function(data){
		username=data.username;
		$("#message_header").append(username);
	});
  url = 'http://localhost:8000/backend/function/messagesBetween/';
  $.post(url,{
    'userA':userID,
    'userB':ID
  },function(messages){
    $(messages).each(function(message){
      if (messages[message]['sender']==userID){
        $("#messages").append("<div id='"+messages[message]['id']+"' class=sentMessage><p class='sentText'>"+messages[message]['msg_content']+"</p></div>");
      }
      else{
        $("#messages").append("<div id='"+messages[message]['id']+"' class=receivedMessage><p class='receivedText'>"+messages[message]['msg_content']+"</p></div>");
      }
    });
  });
}

var mq = window.matchMedia("(min-width: 500px)");

/* Set the width of the side navigation to 300px */
function openItemMenu() {
	windowWidth = $(window).width();
	if (mq.matches) {
		document.getElementById("item_menu").style.width = "300px";
		if (document.getElementById("profile_menu").style.width == "300px"){
			document.getElementById("middle").style.left=String(300)+'px';
			document.getElementById("middle").style.width=String(windowWidth*0.94-600+windowWidth*0.06)+'px';
		}
		else{
			document.getElementById("middle").style.left=String(300)+'px';
			document.getElementById("middle").style.width=String(windowWidth*0.94-300+windowWidth*0.03)+'px';
		}
	} else {
		document.getElementById("item_menu").style.width = "100%";
	}
}


/* Set the width of the side navigation to 300px */
function openProfileMenu() {
	windowWidth = $(window).width();
	if (mq.matches) {
		document.getElementById("profile_menu").style.width = "300px";
		if (document.getElementById("item_menu").style.width == "300px"){
			document.getElementById("middle").style.left=String(300)+'px';
			document.getElementById("middle").style.width=String(windowWidth*0.94-600+windowWidth*0.06)+'px';
		}
		else{
			document.getElementById("middle").style.left=String(windowWidth*0.03)+'px';
			document.getElementById("middle").style.width=String(windowWidth*0.94-300+windowWidth*0.03)+'px';
		}
	} else {
		document.getElementById("profile_menu").style.width = "100%";
	}
}

function logOut()
{
	document.cookie = "authToken=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;";
	window.location.replace("index.html");
}

/* Set the width of the side navigation to 0 */
function closeProfileMenu() {
	windowWidth = $(window).width();
	document.getElementById("profile_menu").style.width = "0";
	if (document.getElementById("item_menu").style.width == "300px"){
		document.getElementById("middle").style.left=String(300)+'px';
		document.getElementById("middle").style.width=String(windowWidth*0.94-300+windowWidth*0.03)+'px';
	}
	else{
		document.getElementById("middle").style.left=String(windowWidth*0.03)+'px';
		document.getElementById("middle").style.width=String(windowWidth*0.94)+'px';
	}
}



/* Set the width of the side navigation to 0 */
function closeItemMenu() {
		windowWidth = $(window).width();
    document.getElementById("item_menu").style.width = "0";
		if (document.getElementById("profile_menu").style.width == "300px"){
			document.getElementById("middle").style.left=String(windowWidth*0.03)+'px';
			document.getElementById("middle").style.width=String(windowWidth*0.94-300+windowWidth*0.03)+'px';
		}
		else{
			document.getElementById("middle").style.left=String(windowWidth*0.03)+'px';
			document.getElementById("middle").style.width=String(windowWidth*0.94)+'px';
		}
}

function addItem() {
    /* Maybe go to pop-up? */
}

function updateMessages(userID){
  url = 'http://localhost:8000/backend/function/'+userID+'/';
	$.get(url, function(user){
		username = user.username;
		url = 'http://localhost:8000/backend/user/'+username+'/contacts/';
		$.get(url,function(contacts){
			$(contacts).each(function(item){
				url = 'http://localhost:8000/backend/function/'+contacts[item]+'/';
				$.get(url, function(data){
					name= data.username;
					$('#contacts').append("<div id='"+contacts[item]+"' onclick=getMessages("+contacts[item]+",true)>"+name+"</div>");
					url = 'http://localhost:8000/backend/function/latestMessageBetween/';
					$.post(url,{'a':userID,'b':contacts[item]},function(message){
						console.log(message);
					});
				});
			});
		});
	});
}



function resize(){
	windowWidth = $(window).width();
	if (document.getElementById("profile_menu").style.width == "300px" && document.getElementById("item_menu").style.width == "300px"){
		document.getElementById("middle").style.left=String(300)+'px';
		document.getElementById("middle").style.width=String(windowWidth*0.94-600+windowWidth*0.06)+'px';
	}
	else if (document.getElementById("profile_menu").style.width == "300px") {
		document.getElementById("middle").style.left=String(windowWidth*0.03)+'px';
		document.getElementById("middle").style.width=String(windowWidth*0.94-300+windowWidth*0.03)+'px';
	}
	else if (document.getElementById("item_menu").style.width == "300px") {
		document.getElementById("middle").style.left=String(300)+'px';
		document.getElementById("middle").style.width=String(windowWidth*0.94-300+windowWidth*0.03)+'px';
	}
	else {
		document.getElementById("middle").style.left=String(windowWidth*0.03)+'px';
		document.getElementById("middle").style.width=String(windowWidth*0.94)+'px';
	}
}


// TODO make woork with smaller screen ie when windows overlap
window.onresize = function(event) {
	resize();
};

function sendMessage(sender_id,receiver_id,msg_content){
	url = 'http://localhost:8000/backend/user/messages/add/';
	$.post(url,{
		'sender_id':sender_id,
		'receiver_id':receiver_id,
		'msg_content':msg_content
	},function(data){
		getMessages(receiver_id,false);
		console.log(data);
	});
}

/* ----- MAP ----- */
var testMarkers = [{"id":1, "lat":54.7753, "long":-1.5849, "highlight":true}, {"id":2, "lat":54.7754, "long":-1.586, "highlight":false}]

var map;
var currentLocationMarker;
var currentMarkers = [];
var chosenLocation = {"lat": 54.7753, "long": -1.5849};

function createMap() {
	navigator.geolocation.getCurrentPosition(mapWithCoords, mapWithoutCoords);
}

function mapWithCoords(pos) {
	var mapProp= {
		center:new google.maps.LatLng(pos.coords.latitude, pos.coords.longitude),
		zoom:17,
	};
	chosenLocation = {"lat": pos.coords.latitude, "long": pos.coords.longitude};
	map=new google.maps.Map(document.getElementById("googleMap"),mapProp);
	setCurrentLocationMarker();
	addListeners();
	loadCommunityFood();
}

function mapWithoutCoords(err) {
	var mapProp= {
		center:new google.maps.LatLng(54.7753,-1.5849),
		zoom:17,
	};
	map=new google.maps.Map(document.getElementById("googleMap"),mapProp);
	setCurrentLocationMarker();
	addListeners();
	loadCommunityFood();
}

function addListeners() {
	google.maps.event.addListener(map, 'click', function(event) {
		chosenLocation = {"lat": event.latLng.lat(), "long": event.latLng.lng()};
		removeMarker();
		setCurrentLocationMarker();
		loadCommunityFood();
	});
}

function setCurrentLocationMarker() {
	var markerIcon = "current_location_marker_icon.png";
	var markerPosition = new google.maps.LatLng(chosenLocation["lat"], chosenLocation["long"]);
	currentLocationMarker = new google.maps.Marker({position:markerPosition, icon:markerIcon});
	currentLocationMarker.setMap(map);
}

function removeMarker() {
	currentLocationMarker.setMap(null);
}

function setMarkers(markers) {
	clearMarkers();
	var markerIcon = "marker_icon.png";
	var highlightedMarkerIcon = "highlighted_marker_icon.png";
	for (var i = 0; i < markers.length; i++) {
		console.log(markers[i]);
		var markerPosition = new google.maps.LatLng(markers[i]["lat"], markers[i]["long"]);
		if (markers[i].highlight) {
			var marker = new google.maps.Marker({position:markerPosition, icon:highlightedMarkerIcon, id:markers[i].id});
		}
		else {
			var marker = new google.maps.Marker({position:markerPosition, icon:markerIcon, id:markers[i].id});
		}
		currentMarkers.push(marker);
		google.maps.event.addListener(marker, 'click', function() {
			selectItem(this.id);
		});
        marker.setMap(map);
    }
}

function clearMarkers() {
	for (var i = 0; i < currentMarkers.length; i++ ) {
		currentMarkers[i].setMap(null);
	}
	currentMarkers.length = 0;
}
