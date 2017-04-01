POST
search: keyword, food_type, location [MIGRATED TO FRONT END]
Return all food items in history belonging to user [COMPLETE]
Edit/remove items [COMPLETE]
post food: food_name, quantity, date_listed, food_type, allergens, status, location, user [COMPLETE]
create user account: username, password, email [COMPLETE]
Allow user to change their profile information [COMPLETE]
authentication: create user if not exist; else check [COMPLETE]
Allow user to set preferences [COMPLETE]
notifications: user, preference [COMPLETE]
send message: sender, receiver, message_content, server_cur_date

GET
search by location [COMPLETE]
search for users [COMPLETE]
get all notifications [COMPLETE]
search all messages, read flag; based on current user_id

### To-Do List on Backend
--> Allow image uploads

##### Security Checklist
- PBKDF2 algorithm with a SHA256 hash; no password is stored in plaintext
- Password validators
- Authentication Tokens are hashed, so no user data is transmitted
- Cookie; cross references the cookie with the auth token