def valid_read_all_reports_from_squad():
    return [
    {
        "member": "Matheus",
        "description": "Realizando back-end",
        "spentHours": 4,
        "createdAt": "2025-01-25T13:17:11.489292"
    },
    {
        "member": "Ana",
        "description": "Refatorando API",
        "spentHours": 6,
        "createdAt": "2025-01-23T13:17:10.534334"
    }
    
    ]
    
def valid_read_all_reports_from_employee():
    return [
    {
        "id": 1,
        "description": "Realizando back-end",
        "employeeId": 1,
        "spentHours": 6,
        "createdAt": "2025-01-25T13:17:11.489292"
    },
    {
        "id": 2,
        "description": "Refatorando API",
        "employeeId": 1,
        "spentHours": 8,
        "createdAt": "2025-01-24T10:27:10.534334"
    }
    ]

def valid_create_report():
    return {
        "description": "Relizando testes de integração",
        "employeeId": 1,
        "spentHours": 8,
    }

def invalid_create_report():
    return {
        "description": "Relizando testes unitários",
        "employeeId": 10,
        "spentHours": 8,
    }