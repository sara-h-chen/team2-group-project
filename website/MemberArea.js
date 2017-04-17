var communityFood = [];
var userFood = [];
var preferences = [];

function getCookie(cname)
{
	var name = cname + "=";
	var decodedCookie = decodeURIComponent(document.cookie);
	var ca = decodedCookie.split(';');
	for(var i = 0; i <ca.length; i++) {
		var c = ca[i];
		while (c.charAt(0) == ' ') {
			c = c.substring(1);
		}
		if (c.indexOf(name) == 0) {
			return c.substring(name.length, c.length);
		}
	}
	return "";
}

function loadCommunityFood()
{
	$.get({
		url: "http://sarachen.pythonanywhere.com/backend/food/"+chosenLocation["lat"]+"/"+chosenLocation["long"]+"/",
		headers:{"Authorization":"Token " + getCookie("authToken")},
		success:function(food)
		{
			communityFood = food;
			
			$.get({
				url: "http://sarachen.pythonanywhere.com/backend/user/preferences/",
				headers:{"Authorization":"Token " + getCookie("authToken")},
				success:function(prefs)
				{
					preferences = prefs;
					displayCommunityFood();
				},
				error: function()
				{
					alert("Not logged in");
					window.location.replace("http://community.dur.ac.uk/thomas.preston/website/index.html"); //TODO remove for final online version necesary to comment out for offline testing
				}
			});
		},
		error: function()
		{
			alert("Not logged in");
			window.location.replace("http://community.dur.ac.uk/thomas.preston/website/index.html"); //TODO remove for final online version necesary to comment out for offline testing
		}
	});
}

function displayCommunityFood()
{
	var data = communityFood.slice();
	var markers = [];
	$("#community_item_list").empty();
	
	if($("#community_food_search_box").val() == "")
	{
		for(var j=0; j<preferences.length; ++j)
		{
			for(var i=data.length-1; i>=0; --i)
			{
				if(data[i]["food_type"] == preferences[j]["preference"])
				{
					var imageSource = ""
					if(data[i]["picture"] == 0)
					{
						imageSource = "http://community.dur.ac.uk/thomas.preston/website/defaultImage.jpg";
					}
					else
					{
						imageSource = data[i]["picture"];
					}
					$("#community_item_list").append('<div class="community_item" id="communityItem'+data[i]["id"]+'">\
					<img class="item_img" src="'+imageSource+'" onclick="viewInfo()">\
					<img id="message1" class="message_img" src="message_no_notification.png" onclick="sendMessage()">\
					<h3>' + data[i]["food_name"] +'('+data[i]["quantity"]+')</h3>\
					Type: '+data[i]["food_type"]+'<br>\
					Allergens: '+data[i]["allergens"]+'<br>\
					</div>\
					<br>');
					
					markers.push({"lat":data[i]["latitude"], "long":data[i]["longitude"], "highlight":true, "id":data[i]["id"]});
					
					data.splice(i,1);
				}
			}
		}
		
		for(var i=0; i<data.length; ++i)
		{
			var imageSource = ""
			if(data[i]["picture"] == 0)
			{
				imageSource = "http://community.dur.ac.uk/thomas.preston/website/defaultImage.jpg";
			}
			else
			{
				imageSource = data[i]["picture"];
			}
			$("#community_item_list").append('<div class="community_item" id="communityItem'+data[i]["id"]+'">\
			<img class="item_img" src="'+imageSource+'" onclick="viewInfo()">\
			<img id="message1" class="message_img" src="message_no_notification.png" onclick="sendMessage()">\
			<h3>' + data[i]["food_name"] +'('+data[i]["quantity"]+')</h3>\
			Type: '+data[i]["food_type"]+'<br>\
			Allergens: '+data[i]["allergens"]+'<br>\
			</div>\
			<br>');
			
			markers.push({"lat":data[i]["latitude"], "long":data[i]["longitude"], "highlight":false, "id":data[i]["id"]});
		}
	}
	else
	{
		var searchScores = [];
		var searchTerm = $("#community_food_search_box").val();
		
		for(var i=0; i<data.length; ++i)
		{
			var score=0;
			for(var j=0; j<=(data[i]["food_name"].length - searchTerm.length); j++)
			{
				if(data[i]["food_name"].substring(j, j+searchTerm.length).toLowerCase() == searchTerm.toLowerCase())
				{
					score++;
				}
			}
			
			searchScores.push(score);
		}
		
		for(var i=data.length-1; i>=0; --i)
		{
			if(searchScores[i] == 0)
			{
				data.splice(i,1);
				searchScores.splice(i,1);
			}
		}
		
		for(var i=0; i<data.length; ++i)
		{
			var imageSource = ""
			if(data[i]["picture"] == 0)
			{
				imageSource = "http://community.dur.ac.uk/thomas.preston/website/defaultImage.jpg";
			}
			else
			{
				imageSource = data[i]["picture"];
			}
			$("#community_item_list").append('<div class="community_item" id="communityItem'+data[i]["id"]+'">\
			<img class="item_img" src="'+imageSource+'" onclick="viewInfo()">\
			<img id="message1" class="message_img" src="message_no_notification.png" onclick="sendMessage()">\
			<h3>' + data[i]["food_name"] +'('+data[i]["quantity"]+')</h3>\
			Type: '+data[i]["food_type"]+'<br>\
			Allergens: '+data[i]["allergens"]+'<br>\
			</div>\
			<br>');
			
			var isPref = false;
			
			for(var j=0; j<preferences.length; ++j)
			{
				if(preferences[j]["preference"] == data[i]["food_type"])
				{
					isPref = true;
				}
			}
			
			markers.push({"lat":data[i]["latitude"], "long":data[i]["longitude"], "highlight":isPref, "id":data[i]["id"]});
		}
	}

	setMarkers(markers);
}

var currentSearch = "";

function checkSearch()
{
	if($("#community_food_search_box").val() != currentSearch)
	{
		currentSearch = $("#community_food_search_box").val();
		displayCommunityFood();
	}
}

setInterval(checkSearch, 500);

function selectItem(id)
{
	for(var i=0; i<communityFood.length; ++i)
	{
		$("#communityItem" + communityFood[i]["id"]).css('background-color', '#222222');
	}

	$("#communityItem" + id).css('background-color', 'green');
	$("#communityItem" + id).get(0).scrollIntoView();
}

function showUserFood()
{
	$("#user_item_list").empty();
	$("#new_food_form").hide();
	$("#user_item_list").show();

	$.get({
		url: "http://sarachen.pythonanywhere.com/backend/user/history/",
		headers:{"Authorization":"Token " + getCookie("authToken")},
		success:function(data)
		{
			userFood = data;

			$("#user_item_list").append("Your Items:<br>");

			for(var i=0; i<data.length; ++i)
			{
				$("#user_item_list").append('<div class="user_item" id="userFoodItem'+data[i]["id"]+'">\
				<img id="del1" class="del_img" src="delete_icon.png" onclick="deleteFoodItem('+data[i]["id"]+')">\
				<img id="edit1" class="edit_img" src="edit_icon.png" onclick="showEditFoodForm('+data[i]["id"]+')">\
				<img id="type1" class="type_img" src="veg_icon.png">\
				<h3 class="item_name">' + data[i]["food_name"] +'('+data[i]["quantity"]+')</h3>\
				Type: '+data[i]["food_type"]+'<br>\
				Allergens: '+data[i]["allergens"]+'<br>\
				</div>');
			}

			if(data.length == 0)
			{
				$("#user_item_list").append("No items");
			}
		},
		error: function()
		{
			alert("Not logged in");
			// window.location.replace("http://community.dur.ac.uk/thomas.preston/website/index.html");
		}
	});
	editing = -1;
}
showUserFood();

function showNewFoodForm()
{
	image="0";
	$("#new_food_name").val("");
	$("#new_food_quantity").val("");
	$("#new_food_type").val("");
	$("#new_food_allergens").val("");
	$("#user_item_list").hide();
	$("#new_food_form").show();
	$("#uploadImage").remove();
	$("#add_food_button").before("<div id='uploadImage'>Image(optional): <input type='file' id='new_food_image' accept='image/*' onchange='readImage(event)'></div>");
}

var editing = -1;

function showEditFoodForm(id)
{
	editing = id;
	$("#new_food_name").val("");
	$("#new_food_quantity").val("");
	$("#new_food_type").val("");
	$("#new_food_allergens").val("");
	$("#uploadImage").remove();
	for(var i=0; i<userFood.length; ++i)
	{
		if(userFood[i]["id"] == editing)
		{
			$("#new_food_name").val(userFood[i]["food_name"]);
			$("#new_food_quantity").val(userFood[i]["quantity"]);
			$("#new_food_type").val(userFood[i]["food_type"]);
			$("#new_food_allergens").val(userFood[i]["allergens"]);
			break;
		}
	}
	$("#user_item_list").hide();
	$("#new_food_form").show();
}

var image = "0";
function readImage(event)
{
	var file = event.target.files[0];
	if(file.size > 30000)
	{
		alert("Image too large (30kB limit)");
		image = "0";
		return;
	}

	var reader = new FileReader();

	reader.onload = function(event)
	{
		image = event.target.result;
	};

	reader.onerror = function()
	{
		image = "0";
	};

	reader.readAsDataURL(file);
}

function deleteFoodItem(id)
{
	$("#userFoodItem" + id).remove();
	$.ajax({
		url: "http://sarachen.pythonanywhere.com/backend/food/update/"+id+"/",
		method:"DELETE",
		headers:{"Authorization":"Token " + getCookie("authToken")},
		success:function(data)
		{
			loadCommunityFood();
		},
		error: function()
		{
			alert("Not logged in");
			// window.location.replace("http://community.dur.ac.uk/thomas.preston/website/index.html");
		}
	});
}

function addNewFood()
{
	if(editing == -1)
	{
		var latitude = chosenLocation["lat"].toFixed(6);
		var longitude = chosenLocation["long"].toFixed(6);

		var food;
		if(image == "0")
		{
			food = {"food_name" : $("#new_food_name").val(), "quantity" : $("#new_food_quantity").val(), "food_type" : $("#new_food_type").val(), "allergens" : $("#new_food_allergens").val(), "status" : "AVAILABLE", "latitude" : latitude, "longitude" : longitude};
		}
		else
		{
			food = {"food_name" : $("#new_food_name").val(), "quantity" : $("#new_food_quantity").val(), "food_type" : $("#new_food_type").val(), "allergens" : $("#new_food_allergens").val(), "status" : "AVAILABLE", "latitude" : latitude, "longitude" : longitude, "picture":image};
		}

		$.post({
			url: "http://sarachen.pythonanywhere.com/backend/food/1.0/1.0/",
			data: JSON.stringify(food),
			contentType: "application/json",
			headers:{"Authorization":"Token " + getCookie("authToken")},
			dataType: "json",
			success:function(data)
			{
				showUserFood();
				loadCommunityFood();
				editing = -1;
			},
			error: function()
			{
				alert("Not logged in");
				// window.location.replace("http://community.dur.ac.uk/thomas.preston/website/index.html");
			}
		});
	}
	else
	{
		var food = {"food_name" : $("#new_food_name").val(), "quantity" : $("#new_food_quantity").val(), "food_type" : $("#new_food_type").val(), "allergens" : $("#new_food_allergens").val(), "status" : "AVAILABLE"};

		$.ajax({
			url: "http://sarachen.pythonanywhere.com/backend/food/update/"+editing+"/",
			method:"PUT",
			data: JSON.stringify(food),
			contentType: "application/json",
			headers:{"Authorization":"Token " + getCookie("authToken")},
			dataType: "json",
			success:function(data)
			{
				showUserFood();
				loadCommunityFood();
				editing = -1;
			},
			error: function()
			{
				alert("Not logged in");
				// window.location.replace("http://community.dur.ac.uk/thomas.preston/website/index.html");
			}
		});
	}
}
