# Faceauth
## Project overview
It's (or it's meant to be) a library, which lets you add authorization using face recognition to your app.

It consists of following parts:
1. Auth model, which should be created in a way that can be easily integrated with any Django Auth
2. Frontend, which should be capable of using a webcam, and send taken photo to the backend (in the first iteration, it will be done in Django templates, but later on we may want to migrate to Expo, so that it could be easily integrated with web, mobile, macOS and windows standalone apps)
3. ML-based model, which should be capable of recognizing, if a photo of a face belongs to a user

## Installation

1. Create a virtual environment, using `virtualenv`, `pipenv`, or whatever you like (Python version: 3.11)
2. Clone this repo: `git clone git@github.com:5ZYSZ3K/faceauth.git`
3. Install requirements: `pip install -r requirements.txt`
4. Migrate the database: `python manage.py migrate`
5. Start the project: `python manage.py runserver 0.0.0.0:8000`
6. To run od Windows config your git first. Run: `git config --local core.autocrlf false`
   



## Contributing and project management

Feel free to start PRs, but until the project review date, I will most likely reject them right away
Anyway, the list of ongoing tasks is in the `Issues` tab
