#!/usr/bin/env python

from flask import Flask, Response
import sqlite3
import json

app = Flask(__name__)
app.config.from_envvar('FORTUNE_SERVICE_CONFIG')
if app.debug is not True:
    import logging
    from logging.handlers import RotatingFileHandler

    file_handler = RotatingFileHandler('/tmp/fortune_service.log',
                                       maxBytes = 10 * 1024 * 1024,
                                       backupCount = 20)
    file_handler.setLevel(logging.ERROR)
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    file_handler.setFormatter(formatter)
    app.logger.addHandler(file_handler)

def get_random_fortune(db):
    for row in db.execute('select id, body from fortunes '
                          'order by random() limit 1'):
        return row

def dict_as_response(dictionary):
    return Response(json.dumps(dictionary, indent=4, separators=(',', ': ')),
                    mimetype='application/json')

def fortune_response(fortune_id, fortune_body):
    return dict_as_response({'id': fortune_id,
                             'body': fortune_body,
                             'status': 'ok'})

def not_found_response():
    return dict_as_response({'status': 'not_found'})

@app.route('/api/random')
def route_api_random():
    with sqlite3.connect(app.config['DATABASE']) as db:
        random_fortune = get_random_fortune(db)
        print random_fortune
        if random_fortune != None:
            (fortune_id, fortune_body) = random_fortune
            return fortune_response(fortune_id, fortune_body)
        else:
            return not_found_response()

if __name__ == '__main__':
    app.run()
