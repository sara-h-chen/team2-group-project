POST
search: keyword, food_type, location
post food: food_name, quantity, date_listed, food_type, allergens, status, location, user [done]
send message: sender, receiver, message_content, server_CUR_DATE
create user account: username, password, email
notifications: user, food_type
read notifications: mark read

GET
search all current food ever in the world [returns by location]
search by location [done]
search all messages, read flag; based on current user_id
search users [done]
get all notifications [counts notifications]