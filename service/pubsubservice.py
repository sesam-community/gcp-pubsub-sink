import os
import logging
import json
import cherrypy
from flask import Flask, request, Response
from google.cloud import pubsub_v1

app = Flask(__name__)

PROJECT_ID = os.environ.get('PROJECT_ID')
CREDENTIALS_PATH = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
CREDENTIALS = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS_CONTENT")

log_level = logging.getLevelName(os.environ.get("LOG_LEVEL", "ERROR"))
logging.basicConfig(level=log_level)

if not PROJECT_ID:
    logging.error("Google cloud platform project id is undefined")

if CREDENTIALS:
    with open(CREDENTIALS_PATH, "wb") as out_file:
        out_file.write(CREDENTIALS.encode())


@app.route('/', methods=['POST'])
def process():

    topic_name = os.environ.get("TOPIC")
    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(PROJECT_ID, topic_name)
    input_data = request.get_json()

    def generate():
        yield "["
        for index, input_entity in enumerate(input_data):
            output_entity = dict()
            output_entity['_id'] = input_entity['_id']
            if index > 0:
                yield ","
            data = json.dumps(input_entity).encode("utf-8")
            try:
                publisher.publish(topic_path, data=data)
            except Exception as e:
                logging.error(e)
                output_entity['result'] = "ERROR: {}".format(str(e))
            yield json.dumps(output_entity)
        yield "]"

    return Response(generate(), content_type="application/json")


if __name__ == '__main__':
    cherrypy.tree.graft(app, '/')

    # Set the configuration of the web server to production mode
    cherrypy.config.update({
        'environment': 'production',
        'engine.autoreload_on': False,
        'log.screen': True,
        'server.socket_port': 5000,
        'server.socket_host': '0.0.0.0'
    })

    # Start the CherryPy WSGI web server
    cherrypy.engine.start()
    cherrypy.engine.block()
