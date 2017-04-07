var communityFood = [];

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
				$("#community_item_list").append('<div class="community_item">\
				<img class="item_img" src="example_tomato.jpg" onclick="viewInfo()">\
				<img id="message1" class="message_img" src="message_no_notification.png" onclick="sendMessage()">\
				<h3>' + communityFood[i]["food_name"] +'</h3>\
				</div>\
				<br>');
			}
		},
		error: function(){alert("Not logged in");}
	});
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
			$("#user_item_list").append("Your Items:<br>");
			
			for(var i=0; i<data.length; ++i)
			{
				$("#user_item_list").append('<div class="user_item" id="userFoodItem'+data[i]["id"]+'">\
				<img id="del1" class="del_img" src="delete_icon.png" onclick="deleteFoodItem('+data[i]["id"]+')">\
				<img id="edit1" class="edit_img" src="edit_icon.png">\
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
}
showUserFood();

function showNewFoodForm()
{
	$("#user_item_list").hide();
	$("#new_food_form").show();
}

function deleteFoodItem(id)
{
	$("#userFoodItem" + id).remove();
	$.ajax({
		url: "http://sarachen.pythonanywhere.com/backend/food/update/"+id+"/",
		method:"DELETE",
		headers:{"Authorization":"Token " + getCookie("authToken")}
	});
}

function addNewFood()
{
	var food = {"food_name" : $("#new_food_name").val(), "quantity" : $("#new_food_quantity").val(), "food_type" : "VEGE", "allergens" : "NUTS", "status" : "AVAILABLE", "latitude" : chosenLocation["lat"], "longitude" : chosenLocation["long"]};
			
	$.post({
		url: "http://sarachen.pythonanywhere.com/backend/food/1.0/1.0/",
		data: JSON.stringify(food),
		contentType: "application/json",
		headers:{"Authorization":"Token " + getCookie("authToken")},
		dataType: "json",
		success:function(data)
		{
			showUserFood();
		}
	});
}
