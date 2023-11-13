# NextGeni_Assignmet2_Blog_App

**Blog_app.py**

This file contains the Flask server and all the Rest Apis

 `token_required Decorator`
The token_required decorator is a utility function designed for use in a Flask web application.
It is used to protect specific routes or views by ensuring that an authentication token is provided in the request. 

`register_user` Endpoint

The /register endpoint in the Flask application is designed for user registration. It accepts the user's email and password as query parameters and performs the following actions:

1. Validate the provided email address using the validate_email function.
2. Checks for duplicate email addresses in the user database using the check_for_email_duplicates method.
3. Registers a new user if the email address is valid and not already in use.


`/login` Endpoint

The /login endpoint in the Flask application is designed for user authentication. It accepts user credentials (email and password) through a POST request and performs the following actions:

1. Attempts to authenticate the user by calling the user_login method.
2. If the authentication is successful, it generates a JSON Web Token (JWT) containing the user's email and an expiration timestamp.
3. Respond with the generated token.




`/add_blog` Endpoint

The /add_blog endpoint in the Flask application is designated for adding new blog entries. It accepts a POST request, requires authentication using a token (as indicated by the @token_required decorator), and performs the following actions:

1. Retrieves user email and blog data from the request.
2. Calls the create_blog method to add a new blog entry associated with the provided user email and blog data.
3. Responds with the newly created blog's ID if successful.




`/blog/add_comment` Endpoint

The /blog/add_comment endpoint in the Flask application is designed for adding comments to a specific blog entry. It requires a POST request, authenticates the user using a token (as indicated by the @token_required decorator), and performs the following actions:

1. Retrieves the blog ID and comment data from the request.
2. Calls the create_comment method to add a new comment associated with the provided blog ID and comment data.
3. Responds with the ID and content of the newly created comment if successful.


**model.py**

This file contains all the function for Database operations.
