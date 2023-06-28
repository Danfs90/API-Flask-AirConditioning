import sqlite3
from controller import OpenWeather
from datetime import datetime



class Context:
    city = "curitiba"

    def __init__(self):
        self.conn = sqlite3.connect('weather.db')
                
    @classmethod
    def defined_city(cls, city):
        obj = cls()  
        obj.city = city
        v1 = obj.insert()  
        return v1
    
    def city_global(cls):

        return cls.city
    
    def insert(self):
        now = datetime.now()
        now = now.strftime('%Y-%m-%d %H:%M:%S')

        city = self.city_global()
        temp_ambient = OpenWeather(self.city).weather()
        temp_ambient = int(temp_ambient['temperatura'])  

        row = self.select()
        status = int(row.get("id_status"))
        temp = int(row.get("air_airconditioning"))
        scheduler = row.get("scheduler")

        if status == 1:
            on = "connected"
        else:
            on = "unconnected"

        self.conn.execute("INSERT INTO WEATHER (AMBIENT, AIR_CONDITIONING, ID_STATUS, MODIFICATION,SCHEDULED,CITY) VALUES (?, ?, ?, ?,?,?)", (temp_ambient, temp, status, now,scheduler,city))

        self.conn.commit()                
        return {"status_response": 200,"air_airconditioning":temp,"ambient":temp_ambient,"id_status":status,"status":on,"modificated":now,"scheduler":scheduler,"city":city}


    def insert_scheduler(self,scheduler):
        try:
            now = datetime.now()
            now_datatime = now.strftime('%Y-%m-%d %H:%M:%S')
            now = now.strftime('%Y-%m-%d')
            scheduler = now + ' ' + scheduler

            row = self.select()
            status = int(row.get("id_status"))
            temp = int(row.get("air_airconditioning"))
            city = row.get("city")

            temp_ambient = OpenWeather(city).weather()
            temp_ambient = int(temp_ambient['temperatura'])


            self.conn.execute("INSERT INTO WEATHER (AMBIENT, AIR_CONDITIONING, ID_STATUS, MODIFICATION,SCHEDULED,CITY) VALUES (?, ?, ?, ?,?,?)", (temp_ambient, temp, status, now_datatime  ,scheduler,city))
            self.conn.commit()

            return {"status": 200, "execution": "Insert Success"}
        except sqlite3.Error as e:
            return {"status": 500, "execution": f"Error inserting data: {e}"}

    def update(self,temp):
        try:
            row = self.select()
            now = datetime.now()
            now = now.strftime('%Y-%m-%d %H:%M:%S')

            city = row.get("city")

            temp_ambient = OpenWeather(city).weather()
            temp_ambient = int(temp_ambient['temperatura'])

            status = int(row.get("id_status"))


            if status == 1:

                scheduler = row.get("scheduler")
                
                if scheduler == None:
                    scheduler = None
                
                on = "connected"
                self.conn.execute("INSERT INTO WEATHER (AMBIENT, AIR_CONDITIONING, ID_STATUS, MODIFICATION,SCHEDULED,CITY) VALUES (?, ?, ?, ?,?,?)", (temp_ambient, int(temp), status, now,scheduler,city))

                self.conn.commit()
                return {"status_response": 200,"air_airconditioning":temp,"ambient":temp_ambient,"id_status":status,"status":on,"modificated":now,"scheduler":scheduler,"city":city}
            else:
                on = "unconnected"
                return {"status_response": 200,"error":"device off"}


        except sqlite3.Error as e:
            return {"status": 500, "execution": f"Error updating data: {e}"}

    def update_status(self,status):
        try:
            row = self.select()
            now = datetime.now()
            now = now.strftime('%Y-%m-%d %H:%M:%S')

            city = row.get("city")

            temp_ambient = OpenWeather(city).weather()
            temp_ambient = int(temp_ambient['temperatura'])

            temp = int(row.get("air_airconditioning"))
            scheduler = row.get("scheduler")

            if scheduler == None:
                scheduler = None

            status = int(status)
            print(status)
            if status == 1:
                on = "connected"
            else:
                on = "unconnected"
            self.conn.execute("INSERT INTO WEATHER (AMBIENT, AIR_CONDITIONING, ID_STATUS, MODIFICATION,SCHEDULED,CITY) VALUES (?, ?, ?, ?,?,?)", (temp_ambient, temp, status, now,scheduler,city))

            self.conn.commit()
            return {"status_response": 200,"air_airconditioning":temp,"ambient":temp_ambient,"id_status":status,"status":on,"modificated":now,"scheduler":scheduler,"city":city}

        except sqlite3.Error as e:
            return {"status": 500, "execution": f"Error updating data: {e}"}
        
    def select(self):
        try:
            query = "SELECT * FROM WEATHER ORDER BY MODIFICATION DESC"
            cursor = self.conn.cursor()
            cursor = cursor.execute(query)
            rows = cursor.fetchone()
            if rows[3] == 1:
                on = "connected"
            else:
                on = "unconnected"

            if rows[5] == None:
                scheduler = "No scheduler"
            else:
                scheduler = rows[5]
                                    
            return {"status_response": 200,"air_airconditioning":rows[2],"ambient":rows[1],"id_status":rows[3],"status":on,"modificated":rows[4],"scheduler":scheduler,"city":rows[6]}
        
        except sqlite3.Error as e:
            return {"status": 500, "execution": f"Error data: {e}"}
        
    def select_all(self):
        try:
            query = "SELECT * FROM WEATHER ORDER BY MODIFICATION DESC"
            cursor = self.conn.cursor()
            cursor.execute(query)
            rows = cursor.fetchall()

            results = []
            for row in rows:
                if row[3] == 1:
                    status = "connected"
                else:
                    status = "unconnected"

                if row[5] is None:
                    scheduler = "No scheduler"
                else:
                    scheduler = row[5]

                result = {
                    "id": row[0],
                    "ambient": row[1],
                    "air_conditioning": row[2],
                    "id_status": row[3],
                    "status": status,
                    "modification": row[4],
                    "scheduler": scheduler,
                    "city":row[6]
                }
                results.append(result)

            return results
        except sqlite3.Error as e:
            return {"status": 500, "execution": f"Error data: {e}"}    
        



