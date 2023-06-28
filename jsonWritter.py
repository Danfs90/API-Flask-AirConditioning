import sqlite3
import json

class JSONResultWriter:
    def __init__(self, filename):
        self.filename = filename

    def write_result(self, result):
        with open(self.filename, 'w') as file:
            json.dump(result, file)

class ContextJson:
    def __init__(self):
        self.conn = None

    def connect(self):
        try:
            self.conn = sqlite3.connect('weather.db')
        except sqlite3.Error as e:
            print(f"Error connecting to database: {e}")

    def disconnect(self):
        if self.conn:
            self.conn.close()

    def select(self):
        try:
            query = "SELECT * FROM WEATHER ORDER BY ID DESC"
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
                    "scheduler": scheduler
                }
                results.append(result)

            return results
        except sqlite3.Error as e:
            return {"status": 500, "execution": f"Error data: {e}"}

    def save_result_to_json(self, filename):
        results = self.select()
        writer = JSONResultWriter(filename)
        writer.write_result(results)
