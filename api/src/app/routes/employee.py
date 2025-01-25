from fastapi import APIRouter, status, Body, HTTPException

from src.utils import Message
from src.models.employee_model import EmployeeBase, EmployeeRead
from src.database.repositories.employee_repository import EmployeeDAO
from src.database.repositories.squad_repository import SquadDAO

router = APIRouter()

@router.post('/create', status_code=status.HTTP_201_CREATED, response_description='Create new employee', response_model=Message)
def create_employee(new_employee: EmployeeBase = Body(...), success_message: str = 'Employee created successfully'):
    squadDAO = SquadDAO()
    squad = squadDAO.read_one_with_id(new_employee.squad_id)
    if squad == None: # If the squad does not exist, return a 409 status code
        raise HTTPException(status_code=404, detail='Squad not found')
    
    employeeDAO = EmployeeDAO()
    employee = employeeDAO.read_one_with_name(new_employee.name)
    if employee: # If the employee already exists, return a 409 status code
        raise HTTPException(status_code=409, detail='Employee with this name already exists')

    created_status = employeeDAO.create(new_employee)

    if not created_status:
        raise HTTPException(status_code=500, detail='Internal server error')

    return Message(message=success_message)

@router.get('/read', status_code=status.HTTP_200_OK, response_description='Read one employee', response_model=EmployeeRead)
def read_one_employee(employee_id: int):
    employeeDAO = EmployeeDAO()
    employee = employeeDAO.read_one_with_id(employee_id)
    if employee == None:
        raise HTTPException(status_code=404, detail='Employee not found')

    # Convert the tuple to a dictionary
    employee = dict(zip(['id', 'name', 'estimatedHours', 'squadId'], employee))
    return employee

@router.get('/read-all', status_code=status.HTTP_200_OK, response_description='Read all employees', response_model=list[EmployeeRead])
def read_all_employees():
    employeeDAO = EmployeeDAO()
    employees = employeeDAO.read_all()
    print(employees)
    if employees == None or employees == []:
        raise HTTPException(status_code=404, detail='No employees found')

    # Convert the list of tuples to a list of dictionaries
    employees = [dict(zip(['id', 'name', 'estimatedHours', 'squadId'], employee)) for employee in employees]
    return employees

