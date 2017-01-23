from flask import render_template, flash, g, Blueprint, redirect, url_for

mod_home = Blueprint('home', __name__)


@mod_home.route('/', methods=['GET'])
def index():
    return render_template('index.html')


# https://www.reddit.com/r/reactjs/comments/42pn95/reactrouter_and_flask_404/
@mod_home.route('/', defaults={'path': ''})
@mod_home.route('/<path:path>')
def catchall(path):

    return render_template('index.html')
