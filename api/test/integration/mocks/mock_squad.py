def valid_create_squad():
    return {
        "name": "back-end"
    }

def valid_read_squad():
    return {
        "id": 1,
        "name": "back-end"
    }

def invalid_create_squad():
    return {
        "name": ""
    }

def squad():
    return {
        "name": "front-end"
    }
    
def read_all_squads():
    return[
        {
            "id": 1,
            "name": "back-end",
        },
        {
            "id": 2,
            "name": "front-end",
        }
    ]
    
def valid_read_spent_hours_response():
    return [
        {
            "employeeId": 1, 
            "employeeName": "Matheus",
            "spentHours": 16
        }, 
        {
            "employeeId": 2, 
            "employeeName": "Ana", 
            "spentHours":8
        }
    ]
def valid_read_total_spent_hours_response():
    return {
            "squadId": 1, 
            "squadName": "back-end",
            "totalHours": 24
    }

def valid_read_average_spent_hours_response():
    return {
            "squadId": 1, 
            "averageHoursPerDay": 2.4
    }