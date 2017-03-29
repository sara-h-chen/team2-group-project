function getMessages(ID){
  $("#messages").empty();
    url = 'http://localhost:8000/backend/function/messagesBetween/';
    $.post(url,{
      'userA':userID,
      'userB':ID
    },function(messages){
      $(messages).each(function(message){
        if (messages[message]['sender']==userID){
          $("#messages").append("<div id='"+messages[message]['id']+"' class=sentMessage>"+messages[message]['msg_content']+"</div>");
        }
        else{
          $("#messages").append("<div id='"+messages[message]['id']+"' class=receivedMessage>"+messages[message]['msg_content']+"</div>");
        }
      });
    });
}

var mq = window.matchMedia("(min-width: 500px)");

/* Set the width of the side navigation to 300px */
function openItemMenu() {
	if (mq.matches) {
		document.getElementById("item_menu").style.width = "300px";
	} else {
		document.getElementById("item_menu").style.width = "100%";
	}
}


/* Set the width of the side navigation to 300px */
function openProfileMenu() {
	if (mq.matches) {
		document.getElementById("profile_menu").style.width = "300px";
	} else {
		document.getElementById("profile_menu").style.width = "100%";
	}
}

function logOut() {
	window.location.href = "index.html";
}

/* Set the width of the side navigation to 0 */
function closeProfileMenu() {
	document.getElementById("profile_menu").style.width = "0";
}



/* Set the width of the side navigation to 0 */
function closeItemMenu() {
    document.getElementById("item_menu").style.width = "0";
}

function addItem() {
    /* Maybe go to pop-up? */
}

function getContacts(userID){
  url = 'http://localhost:8000/backend/function/'+userID+'/';
	$.get(url, function(user){
		username = user.username;
		url = 'http://localhost:8000/backend/user/'+username+'/contacts/';
		$.get(url,function(contacts){
				$(contacts).each(function(item){
					url = 'http://localhost:8000/backend/function/'+contacts[item]+'/';
					$.get(url, function(data){
						name= data.username;
						$('#contacts').append("<div id='"+contacts[item]+"' onclick=getMessages("+contacts[item]+")>"+name+"</div>");
					});
				});
		});
	});
}
