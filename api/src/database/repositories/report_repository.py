import os
import psycopg2

def db_connection():
    connection = psycopg2.connect(
        host='db', 
        port= 5432, 
        database=os.getenv('POSTGRES_DB'), 
        user=os.getenv('POSTGRES_USER'), 
        password=os.getenv('POSTGRES_PASSWORD')
    )
    return connection

class ReportDAO:
    def create(self, report):
        try:
            connection = db_connection()
            cursor = connection.cursor()
            
            query = """
                INSERT INTO Report (description, employeeId, spentHours)
                VALUES (%s, %s, %s);
                """
            
            cursor.execute(query, (report.description, report.employee_id, report.spent_hours))
            connection.commit()
            flag = True
        except Exception as e:
            flag = False
            print("Error create report: ", e)
        finally:
            # closing the cursor and the connection
            if connection:
                cursor.close()
                connection.close()
            
            return flag
        
    def read_all_from_employee(self, employee_id):
        try:
            connection = db_connection()
            cursor = connection.cursor()

            query = """
                SELECT * FROM Report WHERE employeeId = %s;
                """
            cursor.execute(query, (employee_id,))
            connection.commit()
            reports = cursor.fetchall()
        except Exception as e:
            reports = None
            print("Error read all reports with employee id: ", e)
        finally:
            # closing the cursor and the connection
            if connection:
                cursor.close()
                connection.close()
            
            return reports
        
    def read_all_reports_from_squad(self, squad_id, start_date, end_date):
        try:
            connection = db_connection()
            cursor = connection.cursor()

            query = """
                SELECT 
                    e.name AS employee_name,
                    r.description AS description,
                    r.spentHours AS spent_hours,
                    r.createdAt AS created_at
                FROM 
                    Employee e
                INNER JOIN 
                    Report r ON e.id = r.employeeId
                WHERE 
                    e.squadId = %s
                    AND r.createdAt BETWEEN %s AND %s
                ORDER BY 
                    r.createdAt DESC;
                """
            cursor.execute(query, (squad_id, start_date, end_date))
            connection.commit()
            reports = cursor.fetchall()
        except Exception as e:
            reports = None
            print("Error read all reports with employee id: ", e)
        finally:
            # closing the cursor and the connection
            if connection:
                cursor.close()
                connection.close()
            
            return reports
        
