POST
search: keyword, food_type, location [MIGRATED TO FRONT END]
post food: food_name, quantity, date_listed, food_type, allergens, status, location, user [COMPLETE]
create user account: username, password, email [COMPLETE]
authentication: create user if not exist; else check [COMPLETE]
notifications: user, food_type
send message: sender, receiver, message_content, server_cur_date

GET
search all current food ever in the world [returns by current location specified in URL]
search by location [COMPLETE]
search for users [COMPLETE]
get all notifications; counts notifications
search all messages, read flag; based on current user_id

### To-Do List on Backend
Search for food based on keywords or location? [MIGRATED TO FRONT END]
Edit/remove items [done; waiting on testing]
Return all food items belonging to user [done; waiting on testing]
Add authentication to all layers
Allow user to change their profile information
--> allow display pictures?

##### Security Checklist
- PBKDF2 algorithm with a SHA256 hash; no password is stored in plaintext
- Password validators
- Authentication Tokens are hashed, so no user data is transmitted
- Cookie; cross references the cookie with the auth token