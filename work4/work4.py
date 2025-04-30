"""
Flask application for sign-in functionality.

This module contains a simple Flask application with routes for home page, sign-in form, and sign-in processing.
"""

from flask import Flask, request

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    """
    Home page route.

    Returns:
        str: HTML content for the home page.
    """
    return "<h1>Home</h1>"

@app.route("/signin", methods=["GET"])
def signin_form():
    """
    Sign-in form page route.

    Returns:
        str: HTML content for the sign-in form page.
    """
    return '''
        <form action="/signin" method="post">
            <p><input name="username"></p>
            <p><input name="password" type="password"></p>
            <p><button type="submit">Sign In</button></p>
        </form>
    '''

@app.route("/signin", methods=["POST"])
def signin():
    """
    Sign-in processing route.

    Returns:
        str: HTML content indicating success or failure of sign-in.
    """
    # Retrieve username and password from the form data
    username = request.form.get("username")
    password = request.form.get("password")

    # Check if the username and password are correct
    if username == "admin" and password == "password":
        return "<h3>Hello, admin!</h3>"
    return "<h3>Bad username or password.</h3>"

if __name__ == "__main__":
    app.run()
    