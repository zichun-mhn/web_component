from flask import Flask, request, render_template_string,jsonify
import jwt
import datetime
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/display', methods=['POST'])
def display():
    token = request.json  # Get the JWT from the POST request
    try:
        # Decode the JWT without verification
        data = jwt.decode(token, options={"verify_signature": False})
        
        # Check if the token is expired
        if 'exp' in data:
            exp = datetime.datetime.utcfromtimestamp(data['exp'])
            if exp < datetime.datetime.utcnow():
                return jsonify({"error": "Token has expired"}), 401
      
      
        username = data.get('name')
        email = data.get('email')

        # Render the HTML template with the extracted data
        return render_template_string('''
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <title>User Info</title>
            </head>
            <body>
                <h1>User Information</h1>
                <p>Username: {{ username }}</p>
                <p>Email: {{ email }}</p>
            </body>
            </html>
        ''', username=username, email=email)
    except jwt.DecodeError:
        return {"error": "Invalid token"}, 401

if __name__ == '__main__':
    app.run(debug=True)
