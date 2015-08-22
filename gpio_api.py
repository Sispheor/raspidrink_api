from flask import Flask
from flask_restful import Resource, Api
from make_celery import make_celery
from tasks import *
app = Flask(__name__)

# Celery configuration
app.config['CELERY_BROKER_URL'] = 'amqp://guest@localhost//'
app.config['CELERY_RESULT_BACKEND'] = 'amqp://guest@localhost//'

# Initialize Celery
celery = make_celery(app)

# Initialize REST API
api = Api(app)


class HelloWorld(Resource):
    def get(self):
        add_together.delay(1, 2)
        return {'hello': 'world'}

api.add_resource(HelloWorld, '/')


# Run Flask
if __name__ == '__main__':
    app.run(host='0.0.0.0')
