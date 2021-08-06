# **Local Development Setup**

### Prerequisite
* python == 3.8.10 (https://www.python.org/)

### Setup
* Create venv (Virtual Env)
* Run requirements.txt

### Execution
* run `python main.py` to execute code.
* create `post` req from postman to test. `local_address/api/push_data` and pass `webhook` as payload.


# **Heroku Development Setup**

### Prerequisite
* install heroku (https://devcenter.heroku.com/articles/heroku-cli#download-and-install)

### Setup
* login heroku from terminal i.e heroku login
* set your project and app, in this case project is `yourstreetapp` and app is `airtable-hook`

### Deployment
* git add -A
* git commit -m "your msg"
* git push heroku master or git push heroku main 

### Execution
* create `post` req from postman to test. `https://yourappname.herokuapp.com/api/push_data` and pass `webhook` as payload.

