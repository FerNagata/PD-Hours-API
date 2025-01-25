import os
import psycopg2

from src.models.squad_model import SquadBase

def db_connection():
    connection = psycopg2.connect(
        host='db', 
        port= 5432, 
        database=os.getenv('POSTGRES_DB'), 
        user=os.getenv('POSTGRES_USER'), 
        password=os.getenv('POSTGRES_PASSWORD')
    )
    return connection

class SquadDAO:
    def create(self, squad: SquadBase):
        try:
            connection = db_connection()
            cursor = connection.cursor()
            
            query = """
                INSERT INTO Squad (name)
                VALUES (%s);
                """
            
            cursor.execute(query, (squad.name, ))
            connection.commit()
            
            flag = True
        except Exception as e:
            flag = False
            print("Error create squad: ", e)
        finally:
            # closing the cursor and the connection
            if connection:
                cursor.close()
                connection.close()
            return flag
    
    def read_one_with_id(self, squad_id: int):
        try:
            connection = db_connection()
            cursor = connection.cursor()

            query = """
                SELECT * FROM Squad WHERE id = %s;
                """
            cursor.execute(query, (squad_id,))
            connection.commit()
            squad = cursor.fetchone()
        except Exception as e:
            squad = None
            print("Error read one squad with id: ", e)
        finally:
            # closing the cursor and the connection
            if connection:
                cursor.close()
                connection.close()
            
            return squad
        
    def read_one_with_name(self, name: str):
        try:
            connection = db_connection()
            cursor = connection.cursor()

            query = """
                SELECT * FROM Squad WHERE name = %s;
                """
            cursor.execute(query, (name,))
            connection.commit()
            squad = cursor.fetchone()
        except Exception as e:
            squad = None
            print("Error read one squad with name: ", e)
        finally:
            # closing the cursor and the connection
            if connection:
                cursor.close()
                connection.close()
            
            return squad
        
    def read_all(self):
        try:
            connection = db_connection()
            cursor = connection.cursor()

            query = """
                SELECT * FROM Squad;
                """
            cursor.execute(query)
            connection.commit()
            squads = cursor.fetchall()
        except Exception as e:
            squads = None
            print("Error read all squads: ", e)
        finally:
            # closing the cursor and the connection
            if connection:
                cursor.close()
                connection.close()
            
            return squads
        
    def read_spent_hours_from_squad(self, squad_id: int, start_date: str, end_date: str):
        try:
            connection = db_connection()
            cursor = connection.cursor()
            query = """
            SELECT 
                e.id AS employee_id, 
                e.name AS employee_name,
                SUM(r.spentHours) AS total_hours
            FROM 
                Employee e
            INNER JOIN 
                Report r ON e.id = r.employeeId
            WHERE 
                e.squadId = %s
                AND r.createdAt BETWEEN %s AND %s
            GROUP BY 
                e.id, e.name
            ORDER BY 
                total_hours DESC;
            """
            cursor.execute(query, (squad_id, start_date, end_date))
            results = cursor.fetchall()

        except Exception as e:
            results = None
            print("Error reading spent hours from squads: ", e)
        finally:
            # closing the cursor and the connection
            if connection:
                cursor.close()
                connection.close()

            return results
    
    def read_total_spent_hours_from_squad(self, squad_id: int, start_date: str, end_date: str):
        try:
            connection = db_connection()
            cursor = connection.cursor()
            query = """
            SELECT 
                SUM(r.spentHours) AS total_hours
            FROM 
                Employee e
            INNER JOIN 
                Report r ON e.id = r.employeeId
            WHERE 
                e.squadId = %s
                AND r.createdAt BETWEEN %s AND %s;
            """
            cursor.execute(query, (squad_id, start_date, end_date))
            results = cursor.fetchall()

        except Exception as e:
            results = None
            print("Error reading total amount of spent hours from squads: ", e)
        finally:
            # closing the cursor and the connection
            if connection:
                cursor.close()
                connection.close()

            return results
    
    def read_average_spent_hours_from_squad(self, squad_id: int, start_date: str, end_date: str):
        try:
            connection = db_connection()
            cursor = connection.cursor()
            query = """
            SELECT 
                SUM(r.spentHours) AS total_hours,
                DATE_PART('day', %s::timestamptz - %s::timestamptz) + 1 AS total_days
            FROM 
                Employee e
            INNER JOIN 
                Report r ON e.id = r.employeeId
            WHERE 
                e.squadId = %s
                AND createdAt BETWEEN %s AND %s;
            """
            cursor.execute(query, (end_date, start_date, squad_id, start_date, end_date))
            results = cursor.fetchall()

        except Exception as e:
            results = None
            print("Error reading average spent hours from squads: ", e)
        finally:
            # closing the cursor and the connection
            if connection:
                cursor.close()
                connection.close()

            return results