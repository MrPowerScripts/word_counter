#!/usr/bin/python

import psycopg2
import json
import os
from app.settings import Config

conn_string = "dbname='{0}' user='{1}'".format(
    Config.SQLALCHEMY_DATABASE_URI.split("///")[1], Config.WORD_MATCH_DB_USER)

conn = psycopg2.connect(conn_string)

cursor = conn.cursor()


conn.commit()
