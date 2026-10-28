# Secure Authentication Lab

## 1. Project Overview
This project demonstrates a basic web authentication system
using Python and Flask. It focuses on secure authentication
practices and common login security protections.

## 2. Objectives
- Implement user registration and login.
- Store passwords using secure password hashing.
- Validate username and password inputs.
- Use session-based authentication.
- Implement logout functionality.
- Limit repeated login attempts.
- Display generic error messages for failed login attempts.

## 3. Technologies Used
- Python
- Flask
- Werkzeug Security
- HTML
- Git and GitHub

## 4. Security Features

### Password Hashing
Passwords are hashed using Werkzeug's password hashing
functions instead of being stored as plain text.

### Input Validation
Usernames and passwords are checked against defined
validation rules before registration.

### Session Management
Flask sessions maintain the authenticated user's login state.
The session has a configured expiration time.

### Secure Cookie Settings
HTTPOnly and SameSite cookie settings are enabled.
Secure cookies should be enabled when deploying over HTTPS.

### Login Rate Limiting
The application limits repeated login attempts from
the same IP address within a one-minute window.

### Generic Error Messages
Failed login attempts return a generic message:
"Invalid username or password."

### Logout
The logout route clears the current session.

## 5. Installation and Execution

1. Install Python 3.
2. Open a terminal in the project directory.
3. Install the required dependency:

   pip install -r requirements.txt

4. Start the application:

   python app.py

5. Open the application in a browser:

   http://127.0.0.1:5000

## 6. Testing Results

- Application startup: PASS
- Successful login: PASS
- Logout: PASS
- Invalid password handling: PASS
- Login rate limiting: PASS

## 7. Limitations
This project is an educational demonstration.
User accounts and rate-limit records are stored in memory
and are lost when the application restarts.

The development server and current configuration are not
intended for production deployment. Production use requires
additional protections, persistent storage, HTTPS, a strong
secret key, and robust session and rate-limit management.

## 8. Author
Sivasanthi