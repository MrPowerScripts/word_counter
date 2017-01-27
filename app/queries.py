import datetime
import logging
import requests
import json
import re
from bs4 import BeautifulSoup
from psycopg2.extensions import AsIs
from flask import current_app, g
from urlparse import urlparse
from collections import Counter


def submit_url(data):
    try:
        content_data = {}
        # See if the web content is available before dumping into db
        content_data['raw_content'] = requests.get(data['url']).text
    except requests.exceptions.RequestException as e:
        logging.info(e)
        raise e

    try:
        # Just use the base URL
        data['url'] = urlparse(data['url'])[1]
    except Exception as e:
        logging.info(e)
        raise Exception("no url to parse")

    g.cursor.execute("""
    INSERT INTO urls (url) VALUES (%(url)s)
    ON CONFLICT (url)
    DO UPDATE SET date_modified = (now() at time zone 'utc')
    RETURNING id;
    """, data)

    content_data['url_id'] = g.cursor.fetchone()['id']

    try:
        g.conn.commit()
    except Exception as e:
        logging.info(e)
        g.conn.rollback()
        raise e

    # Break down the site content
    soup = BeautifulSoup(content_data['raw_content'], 'html.parser')

    content_data['text_content'] = ''

    # Get the raw text from the lements
    for e in soup.findAll(["p", "span", "a", "h1", "h2",
                           "h3", "h4", "h5", "h6"]):

        logging.info(e.get_text() + " ")
        content_data['text_content'] += e.get_text() + " "

    # Count all of the words in the content
    content_data['word_counts'] = \
        json.dumps(dict(Counter(w.lower() for w in re.findall(r"\w+",
                   content_data['text_content'], re.UNICODE))))

    # Dump everything into the db
    g.cursor.execute("""
    INSERT INTO url_content (url_id, raw_content, text_content, word_counts)
    VALUES (%(url_id)s, %(raw_content)s, %(text_content)s, %(word_counts)s)
    RETURNING word_counts;
    """, content_data)

    try:
        g.conn.commit()
    except Exception as e:
        logging.info(e)
        g.conn.rollback()
        raise e

    return data['url']


def get_url_data(data):

    g.cursor.execute("""
    SELECT url_content.word_counts::JSON,
           url_content.id,
           EXTRACT(EPOCH FROM url_content.date_created)::int AS date_created,
           urls.url
    FROM urls
    JOIN url_content ON url_content.url_id = urls.id
    WHERE urls.url = %(url)s
    ORDER BY url_content.date_created DESC
    LIMIT 3;
    """, data)

    return g.cursor.fetchall()


def get_recently_updated():

    g.cursor.execute("""
    SELECT urls.url FROM urls
    ORDER BY date_modified DESC
    LIMIT 10
    """)

    return g.cursor.fetchall()
