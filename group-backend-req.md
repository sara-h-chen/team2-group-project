POST
search: keyword, food_type, location [MIGRATED TO FRONT END]
Return all food items in history belonging to user [COMPLETE]
Edit/remove items [COMPLETE]
post food: food_name, quantity, date_listed, food_type, allergens, status, location, user [COMPLETE]
create user account: username, password, email [COMPLETE]
authentication: create user if not exist; else check [COMPLETE]
notifications: user, preference
send message: sender, receiver, message_content, server_cur_date

GET
search by location [COMPLETE]
search for users [COMPLETE]
get all notifications
search all messages, read flag; based on current user_id

### To-Do List on Backend
Allow user to set preferences [done; waiting on testing]
Allow user to change their profile information [done; waiting on testing]
--> allow display pictures? Change model to include URL

##### Security Checklist
- PBKDF2 algorithm with a SHA256 hash; no password is stored in plaintext
- Password validators
- Authentication Tokens are hashed, so no user data is transmitted
- Cookie; cross references the cookie with the auth token