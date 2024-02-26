
# Voting System - Deep Face 

This is a web-based voting software system developed using Django. It allows users to register, log in, and cast their votes securely.

## Deployment

To deploy this project,

    1. Navigate to the my_django_project directory
    2. Type "env\Scripts\activate"
    3. Run the command "pip install ." 
    4. Once everything is installed properly, Go to next Step
    5. Run python manage.py runserver 

2 step Install 

  Download and Install Anaconda Navigator

```bash
  pip install .
  python manage.py runserver
```
## Features
- User registration and login system
- Secure authentication using digital IDs
- Capture and compare user photos for authentication
- Vote casting functionality
- Admin panel for managing users and elections

## Usage/Examples

```
Usage
- Register as a new user or log in with existing credentials.
- Capture a photo using the webcam for authentication (if enabled).
- Cast your vote in the available elections.
- Administrators can access the admin panel at 
  http://localhost:8000/admin/ to manage users and elections.

```
## Tech Stack

- Django: Web framework for building the application
- Python: Programming language used for backend development
- HTML/CSS: Frontend languages for designing the user interface
- Bootstrap: Frontend framework for responsive design
- JavaScript: Programming language for client-side functionality
- DeepFace: Python library for facial recognition

