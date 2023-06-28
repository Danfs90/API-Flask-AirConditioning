from controller import OpenWeather
from datetime import datetime
from dbContext import Context
import time
import sched

class Scheduler:

    def __init__(self):
        self.scheduler = sched.scheduler(time.time, time.sleep)

    def monitor_temperature(self):
            row = Context().select()
            status = int(row.get("id_status"))
            city = row.get("city")            
            print(city)
            weather = OpenWeather(city).weather()
            temperatura = weather['temperatura']

            
            if temperatura > 23 and status == 0:
                Context().update_status(1)
                print("Status altered")


            self.scheduler.enter(300, 1, self.monitor_temperature)
            print("In Running temperature")

    def monitor_scheduler(self):
            row = Context().select()
            status = int(row.get("id_status"))
            date_scheduler = row.get("scheduler") 

            now = datetime.now()
            now = now.strftime('%Y-%m-%d %H:%M:%S')

            
            if date_scheduler == now and status == 1:
                Context().update_status(0)
                print("Status altered")


            self.scheduler.enter(1, 1, self.monitor_scheduler)
            print("In Running scheduler")


    def start_monitoring(self):
            
            self.scheduler.enter(0, 1, self.monitor_temperature)
            self.scheduler.enter(0, 1, self.monitor_scheduler)

            self.scheduler.run()

            return {"status":200,"information":"scheduler connected"}

if __name__ == '__main__':
    Scheduler().start_monitoring()