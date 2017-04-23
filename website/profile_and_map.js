function sortList(){
	setTimeout(function () {
        tinysort('#message_list > div',{attr: 'id', order:'desc'});
    }, 500);
}

function getMessages(ID){
	contact=ID;
	windowWidth = $(window).width();
	if (windowWidth<800){
		closeItemMenu();
		closeProfileMenu();
		document.getElementById("message_reload").style.left = '0%';
		document.getElementById("message_reload").style.top = '1%';
	}
  	$("#messages").empty();
	$("#message_header").empty();
	var init;
	if (!($("#message_popup").is(":visible"))){
		$("#message_popup").toggle();
	}
	url = 'http://sarachen.pythonanywhere.com/backend/function/'+ID+'/';
	$.get(url, function(data){
		username=data.username;
		$("#message_header").append(username);
	});
  url = 'http://sarachen.pythonanywhere.com/backend/function/messagesBetween/';
  $.post(url,{
    'userA':userID,
    'userB':ID
  },function(messages){
		messages.sort(function(a,b){
			return a['id']-b['id'];
		});
    $(messages).each(function(message){
      if (messages[message]['sender']==userID){
        $("#messages").append("<div id='"+messages[message]['id']+"' class=sentMessage><p class='sentText'>"+messages[message]['msg_content']+"</p></div>");
      }
      else{
        $("#messages").append("<div id='"+messages[message]['id']+"' class=receivedMessage><p class='receivedText'>"+messages[message]['msg_content']+"</p></div>");
      }
    });
  });
	var element = document.getElementById("messages");
	element.scrollTop = element.offsetHeight;
}

function prepareMessage(receiver_username){
	url = 'http://sarachen.pythonanywhere.com/backend/user/search/'+receiver_username+'/';
	$.get(url, function(data){
		messageContact=data.id;
		getMessages(messageContact);
	});
}

function setUserID(ID){
		userID=ID;
		updateMessages(ID)
		sortList();
}

var mq = window.matchMedia("(min-width: 500px)");
var mobile = window.matchMedia("(max-width: 800px)");

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
	updateMessages(userID);
	sortList();
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
	updateMessages(userID);
	sortList();
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
	if (mobile.matches) {
		if (document.getElementById("item_menu").style.width == "300px"){
			/*
			document.getElementById("middle").style.left=String(300)+'px';
			document.getElementById("middle").style.width=String(windowWidth*0.94-300+windowWidth*0.03)+'px';
			*/
			document.getElementById("middle").style.width='86%';/*for mobile tabs*/
			document.getElementById("middle").style.left='7%';
		}
		else{
			/*
			document.getElementById("middle").style.left=String(windowWidth*0.03)+'px';
			document.getElementById("middle").style.width=String(windowWidth*0.94)+'px';
			*/
			document.getElementById("middle").style.width='86%';/*for mobile tabs*/
			document.getElementById("middle").style.left='7%';
		}
	}
	else if (document.getElementById("item_menu").style.width == "300px"){
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
	if (mobile.matches) {
		if (document.getElementById("profile_menu").style.width == "300px"){
			document.getElementById("middle").style.left=String(windowWidth*0.03)+'px';
			document.getElementById("middle").style.width=String(windowWidth*0.94-300+windowWidth*0.03)+'px';
			document.getElementById("middle").style.width='86%';/*for mobile tabs*/
			document.getElementById("middle").style.left='7%';
		}
		else{
			document.getElementById("middle").style.left=String(windowWidth*0.03)+'px';
			document.getElementById("middle").style.width=String(windowWidth*0.94)+'px';
			document.getElementById("middle").style.width='86%';/*for mobile tabs*/
			document.getElementById("middle").style.left='7%';
		}
	}
	else if (document.getElementById("profile_menu").style.width == "300px"){
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
	$("#message_list").empty();
  url = 'http://sarachen.pythonanywhere.com/backend/function/'+userID+'/';
	$.get(url, function(user){
		username = user.username;
		url = 'http://sarachen.pythonanywhere.com/backend/user/'+username+'/contacts/';
		$.get(url,function(contacts){
			console.log(contacts);
			contacts.sort(function(a,b){
				return
			})
			$(contacts).each(function(item){
				url = 'http://sarachen.pythonanywhere.com/backend/function/'+contacts[item]+'/';
				$.get(url, function(data){
					name= data.username;
					url = 'http://localhost:8000/backend/function/messagesBetween/';
				  $.post(url,{
				    'userA':userID,
				    'userB':contacts[item]
				  },function(messages){
						var mostRecentMessage;
						var mID =-1;
						var l = messages.length;
						var i;
						for (i=0;i<l;i++){
							if (mID<messages[i]['id']){
								mID= messages[i]['id'];
								mostRecentMessage=messages[i];
							}
						}
						$("#message_list").append("<div onclick='getMessages("+contacts[item]+")' class='message' id='message"+mostRecentMessage['id']+'n'+"'></div>");
						$("#message"+mostRecentMessage['id']+'n').append("<p class='sender_name' id='name"+contacts[item]+"'>"+data.username+"</p>");
						$("#message"+mostRecentMessage['id']+'n').append("<p class='sender_preview'>"+mostRecentMessage['msg_content']+"<p");
						$("#message_list").append("<div style='height:2%; visibility:hidden;' id='"+'message'+mostRecentMessage['id']+"'></div>");
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
	url = 'http://sarachen.pythonanywhere.com/backend/user/messages/add/';
	$.post(url,{
		'sender_id':sender_id,
		'receiver_id':receiver_id,
		'msg_content':msg_content
	},function(data){
		getMessages(receiver_id);
		updateMessages(userID);
		sortList();
	});
}

/* ----- MAP ----- */
var testMarkers = [{"id":1, "lat":54.7753, "long":-1.5849, "highlight":true}, {"id":2, "lat":54.7754, "long":-1.586, "highlight":false}];

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
