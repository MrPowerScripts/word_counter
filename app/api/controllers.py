import requests
import logging
import psycopg2
from flask import g, Blueprint, request, current_app, jsonify, Response
from psycopg2.extras import RealDictCursor
from app.queries import submit_url, get_url_data, get_recently_updated

from app.database import db

mod_api = Blueprint('api', __name__)


@mod_api.before_app_request
def before_request():
    g.conn = psycopg2.connect("dbname='{0}' user='{1}'".format(
        current_app.config["SQLALCHEMY_DATABASE_URI"].split("///")[1],
        current_app.config["WORD_MATCH_DB_USER"]))

    g.cursor = g.conn.cursor(cursor_factory=RealDictCursor)


@mod_api.teardown_app_request
def teardown_request(exception):
    pass


@mod_api.route('/urls', methods=['POST'])
def submit_urls():

    data = request.get_json()

    try:
        return jsonify({"url": submit_url(data)}), 200
    except Exception as e:
        logging.info(e)
        return jsonify({"error": "Failed to submit urls"}), 400


@mod_api.route('/urls/site', methods=['POST'])
def request_site():

    data = request.get_json()

    try:
        return jsonify({"success": get_url_data(data)}), 200
    except Exception as e:
        logging.info(e)
        return jsonify({"error": "Failed to get site data"}), 400


@mod_api.route('/urls/updated', methods=['GET'])
def request_recently_updated():

    try:
        return jsonify({"success": get_recently_updated()}), 200
    except Exception as e:
        logging.info(e)
        return jsonify({"error": "Failed to get recently updated"}), 400
