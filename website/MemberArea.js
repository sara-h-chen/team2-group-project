var communityFood = [];
var userFood = [];

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
	$("#community_item_list").empty();
			
	$.get({
		url: "http://sarachen.pythonanywhere.com/backend/food/"+chosenLocation["lat"]+"/"+chosenLocation["long"]+"/",
		headers:{"Authorization":"Token " + getCookie("authToken")},
		success:function(data)
		{
			communityFood = data;
			
			for(var i=0; i<communityFood.length; ++i)
			{
				$("#community_item_list").append('<div class="community_item" id="communityItem'+communityFood[i]["id"]+'">\
				<img class="item_img" src="example_tomato.jpg" onclick="viewInfo()">\
				<img id="message1" class="message_img" src="message_no_notification.png" onclick="sendMessage()">\
				<h3>' + communityFood[i]["food_name"] +'</h3>\
				</div>\
				<br>');
			}
			
			var markers = [];
			
			for(var i=0; i<communityFood.length; ++i)
			{
				markers.push({"lat":communityFood[i]["latitude"], "long":communityFood[i]["longitude"], "highlight":false, "id":communityFood[i]["id"]});
			}
			
			setMarkers(markers);
		},
		error: function(){alert("Not logged in");}
	});
}

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
				<h3 class="item_name">' + data[i]["food_name"] +'</h3>\
				</div>');
			}
			
			if(data.length == 0)
			{
				$("#user_item_list").append("No items");
			}
		}
	});
	editing = -1;
}
showUserFood();

function showNewFoodForm()
{
	$("#new_food_name").val("");
	$("#new_food_quantity").val("");
	$("#new_food_type").val("");
	$("#new_food_allergens").val("");
	$("#user_item_list").hide();
	$("#new_food_form").show();
}

var editing = -1;

function showEditFoodForm(id)
{
	editing = id;
	$("#new_food_name").val("");
	$("#new_food_quantity").val("");
	$("#new_food_type").val("");
	$("#new_food_allergens").val("");
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
		}
	});
}

function addNewFood()
{
	if(editing == -1)
	{
		var latitude = chosenLocation["lat"].toFixed(6);
		var longitude = chosenLocation["long"].toFixed(6);
	
		var food = {"food_name" : $("#new_food_name").val(), "quantity" : $("#new_food_quantity").val(), "food_type" : $("#new_food_type").val(), "allergens" : $("#new_food_allergens").val(), "status" : "AVAILABLE", "latitude" : latitude, "longitude" : longitude};
			
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
			}
		});
	}
}
