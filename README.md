# Memes website
## Table of contents
* [General info](#general-info)
* [Technologies](#technologies)
* [Setup](#setup)
* [To Do](#to-do)

## General info
Web app for browsing memes from other popular sites such:
* [jbzd.pl](https://jbzdy.pl)
* [kwejk.pl](https://kwejk.pl/)
* [demotywatory.pl](https://demotywatory.pl/)
* [mistrzowie.org](https://mistrzowie.org/)

Currenty supports only 'jbzd.pl' and 'kwejk.pl'.
Newest version is currently on `development` branch.

You can see deployed app on: https://usmiechnij-sie-dev.azurewebsites.net

## Technologies
Project is created with:
* Flask (2.1.1)
* Jinja2 (3.1.1)
* beautifulsoup4 (4.11.1)
* HTML + CSS

## Setup
To run this project locally, you can create Python virtual environment from `requirements.txt`.
```console
python3 -m venv env
```
```console
source env/bin/activate (Bash)
\env\Scripts\activate   (PowerShell)
```
```console
python -m pip install -r requirements.txt
```
Finally run app by typing:
```console
python runserver.py
```
or
```console
export FLASK_APP=runserver.py (Bash)
flask run

$env:FLASK_APP='runserver.py' (PowerShell)
flask run
```

## To Do:
There are still many bugs and huge mess in code, since it was first project ever done in Flask and in group at all.
I have a plan to rebuild the whole project in the future, but first I'll have to convince rest of the team :p. 
