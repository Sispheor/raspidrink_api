## Installd requiered packages
sudo apt-get install python-dev python-pip python-yaml

## Install Flask
sudo pip install flask
sudo pip install flask-restful

## Install Celery
sudo pip install celery

## Install RabbitMQ
sudo apt-get install rabbitmq-server

## Install GPIO library
sudo pip install --upgrade RPi.GPIO

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