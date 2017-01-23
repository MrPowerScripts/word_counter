# -*- coding: utf-8 -*-
"""Application assets."""
from flask_assets import Bundle, Environment

from flask import current_app

css = Bundle(
    'public/css/vendor/font-awesome.min.css',
    Bundle('public/css/app.styl',
           depends='/**/*.styl',
           filters='stylus',
           output='public/css/app.css'),
    filters='cssmin',
    output='public/css/common.css'
)

js = Bundle(
    'public/js/vendor/jquery.min.js',
    'public/js/wordCore.js',
    'public/js/bundle.js',

    filters='jsmin',
    output='public/js/common.js'
)


assets = Environment()

assets.register('js_all', js)
assets.register('css_all', css)
