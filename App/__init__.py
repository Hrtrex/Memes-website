from flask import Flask
from datetime import timedelta

app = Flask(__name__, static_url_path='/static')
app.permanent_session_lifetime = timedelta(minutes=7)

import App.views