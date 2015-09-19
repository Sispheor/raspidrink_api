## Installd requiered packages
sudo apt-get install python-dev python-pip python-yaml

## Install Flask, Celery an GPIO library
```
sudo pip install flask
sudo pip install flask-restful
sudo pip install celery
sudo pip install --upgrade RPi.GPIO
```

## Install RabbitMQ
```
sudo apt-get install rabbitmq-server
```

## Edit settings
Edit the settings file settings.yml and configure your slot in reference to the selected port number over 
the Rpi. The slot number 0 is reserved to the Rpi pin that control the reverse relay.

## Run Celery
```
cd path/to/raspidrink_gpio_api
celery -A gpio_api.celery worker --loglevel=info
```

## Run Flask app
```
cd path/to/raspidrink_gpio_api
python gpio_api.py
```

## Test with curl
```
curl 127.0.0.1:5000
```
This command should return RaspiDrink GPIO API online

## Run some test (optional)
If you want to run more test you can run scripts under the tests folder.
The scrpit test_pumps will set all pin in settings to HIGH durring 1 second and then LOW directly with the GPIO lib without calling the API.
The second script allow you to test each component of the API. Comment out what you want to test.