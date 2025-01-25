import os
import psycopg2

from src.models.employee_model import EmployeeBase

def db_connection():
    connection = psycopg2.connect(
        host='db', 
        port= 5432, 
        database=os.getenv('POSTGRES_DB'), 
        user=os.getenv('POSTGRES_USER'), 
        password=os.getenv('POSTGRES_PASSWORD')
    )
    return connection

class EmployeeDAO:
    def create(self, employee: EmployeeBase):
        try:
            connection = db_connection()
            cursor = connection.cursor()
            
            query = """
                INSERT INTO Employee (name, estimatedHours, squadId)
                VALUES (%s, %s, %s);
                """
            cursor.execute(query, (employee.name, employee.estimated_hours, employee.squad_id))
            connection.commit()

            flag = True
        except Exception as e:
            flag = False
            print("Error create employee: ", e)
        finally:
            # closing the cursor and the connection
            if connection:
                cursor.close()
                connection.close()
            
            return flag
    
    def read_one_with_id(self, employee_id: int):
        try:
            connection = db_connection()
            cursor = connection.cursor()

            query = """
                SELECT * FROM Employee WHERE id = %s;
                """
            cursor.execute(query, (employee_id,))
            connection.commit()
            employee = cursor.fetchone()
        except Exception as e:
            employee = None
            print("Error read one employee: ", e)
        finally:
            # closing the cursor and the connection
            if connection:
                cursor.close()
                connection.close()
            
            return employee
    def read_one_with_name(self, name: str):
        try:
            connection = db_connection()
            cursor = connection.cursor()

            query = """
                SELECT * FROM Employee WHERE name = %s;
                """
            cursor.execute(query, (name,))
            connection.commit()
            employee = cursor.fetchone()
        except Exception as e:
            employee = None
            print("Error read one employee: ", e)
        finally:
            # closing the cursor and the connection
            if connection:
                cursor.close()
                connection.close()
            
            return employee
        
    def read_all(self):
        try:
            connection = db_connection()
            cursor = connection.cursor()

            query = """
                SELECT * FROM Employee;
                """
            cursor.execute(query)
            connection.commit()
            employees = cursor.fetchall()
        except Exception as e:
            employees = None
            print("Error read all employees: ", e)
        finally:
            # closing the cursor and the connection
            if connection:
                cursor.close()
                connection.close()
            
            return employees