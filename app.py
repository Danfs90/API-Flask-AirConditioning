from flask import Flask, request
from datetime import datetime 
from controller import OpenWeather
from dbContext import Context
from jsonWritter import ContextJson,JSONResultWriter
from scheduler import Scheduler

app = Flask(__name__)

#Change temperature
@app.route('/v1/weather/alter-temp/<temp>', methods=['POST'])
def alter_temp(temp):
    v1 = Context().update(int(temp))
    return v1

#Change status
@app.route('/v1/weather/alter-status/<status>', methods=['POST'])
def alter_status(status):
    v1 = Context().update_status(status)
    return v1

#Check current temperature
@app.route('/v1/weather/verify/', methods=['GET'])
def verify():
    v1 = Context().select()
    return v1

#Check all temperatures
@app.route('/v1/weather/verify-all/', methods=['GET'])
def verify_all():
    v1 = Context().select_all()
    return v1

#Add a schedule
@app.route('/v1/weather/schedule-time/<hour>', methods=['POST'])
def schedule_time(hour):

    v1 = Context().insert_scheduler(hour)
    
    return v1

#Create log in json
@app.route('/v1/weather/json-writter/', methods=['GET'])
def get_weather():
    context = ContextJson()
    context.connect()
    context.save_result_to_json("log.json")
    context.disconnect()
    return {"status":200,"information":"log saved"}

#Change the city
@app.route('/v1/weather/defined-city/<city>', methods=['PUT'])
def defined_city(city):
    v1 = Context().defined_city(city)
    v2 = Scheduler().defined_city_scheduler(city)
    return v1

#Check city
@app.route('/v1/cidade/<city>', methods=['POST'])
def weather(city):
    v1 = OpenWeather(city).weather()
    return v1

if __name__ == '__main__':
    app.run(debug=True)