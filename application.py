from flask import Flask, render_template, request, flash, url_for, redirect, abort
import json
import os

application = Flask(__name__)

if 'DEBUG' in os.environ and os.environ['DEBUG'] == '1':
    application.debug = True

@application.route('/')
def do_root():
    return "Index Page"


@application.route('/admin/healthcheck')
def healthcheck():
    return "Hello World!"

if __name__ == '__main__':
        if 'LOCALHOST' in os.environ and os.environ['LOCALHOST'] == '1':
                application.run('0.0.0.0', use_reloader=False)
        else:
                application.run('0.0.0.0')