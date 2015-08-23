from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from make_celery import make_celery
from tasks import *
from FileLock import FileLock
import json
import ast
app = Flask(__name__)

# Celery configuration
app.config['CELERY_BROKER_URL'] = 'amqp://guest@localhost//'
app.config['CELERY_RESULT_BACKEND'] = 'amqp://guest@localhost//'

# Initialize Celery
celery = make_celery(app)

# Initialize REST API
api = Api(app)


def get_highter_volume(slot_volume_dict):
    list_volume = []
    for el in slot_volume_dict:
        list_volume.append(int(el['volume']))
    return max(list_volume)


class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}


class Cocktail(Resource):
    def post(self):
        # check lock file
        filelock = FileLock("raspidrink")
        if filelock.is_valide():
            return {'status': 'working'}
        else:
            # No lock file, we can make the cocktail
            json_data = request.get_json(force=True)
            slot_volume_dict = json_data['data']
            # decode json. This give a string
            slot_volume_dict = json.dumps(slot_volume_dict)
            # use ast to convert str from unicode to a dict
            slot_volume_dict = ast.literal_eval(slot_volume_dict)
            make_cocktail.delay(slot_volume_dict)
            # get highest number in volume list
            bigger_volume = get_highter_volume(slot_volume_dict)
            # create file locker
            filelock = FileLock("raspidrink", timeout=int(bigger_volume))
            filelock.create_lock_file()
            return {'status': 'ok'}


class ReversePump(Resource):
    def post(self):
        # check lock file
        filelock = FileLock("raspidrink")
        if filelock.is_valide():
            return {'status': 'working'}
        else:
            # No lock file, we can reverse all pump
            reverse_pump.delay()
            return {'status': 'ok'}


class Pump(Resource):
    def post(self):
        # check lock file
        filelock = FileLock("raspidrink")
        if filelock.is_valide():
            return {'status': 'working'}
        else:
            # No lock file, we can reverse all pump
            json_data = request.get_json(force=True)
            action = json_data['action']
            try:
                slot_id = json_data['slot_id']
                action = json_data['action']
            except KeyError, e:
                slot_id = None

            pump_management.delay(action, slot_id)
            return {'status': 'ok'}


api.add_resource(HelloWorld, '/')
api.add_resource(Cocktail, '/make_cocktail')
api.add_resource(ReversePump, '/reverse_pump')
api.add_resource(Pump, '/active_pump')

# Run Flask
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
