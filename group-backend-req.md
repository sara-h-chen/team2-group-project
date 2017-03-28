POST
search: keyword, food_type, location [done]
post food: food_name, quantity, date_listed, food_type, allergens, status, location, user [done]
send message: sender, receiver, message_content, server_CUR_DATE
create user account: username, password, email [done]
notifications: user, food_type
authentication: create user if not exist; else check [done]

GET
search all current food ever in the world [returns by location]
search by location [done]
search all messages, read flag; based on current user_id
search users [done]
get all notifications [counts notifications]

### To-Do List on Backend


SHA-256 database; no password is stored in plaintext
Integration with OAuth authentication systems
Password validators