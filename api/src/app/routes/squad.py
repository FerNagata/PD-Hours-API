from fastapi import APIRouter, status, Body, HTTPException, Query
from datetime import datetime
from src.utils import Message
from src.models.squad_model import SquadBase, SquadRead, EmployeeHours, AverageHours, TotalHours
from src.database.repositories.squad_repository import SquadDAO

router = APIRouter()

@router.post('/create', status_code=status.HTTP_201_CREATED, response_description='Create new squad', response_model=Message)
def create_squad(new_squad: SquadBase = Body(...)):
    
    if new_squad.name == "":
        raise HTTPException(status_code=422, detail='Name cannot be an empty string')
        
    squadDAO = SquadDAO()
    squad = squadDAO.read_one_with_name(new_squad.name)
    if squad: # If the squad already exist, return a 409 status code
        raise HTTPException(status_code=409, detail='Squad with this name already exists')
    
    created_status = squadDAO.create(new_squad)

    if not created_status:
        raise HTTPException(status_code=500, detail='Internal server error')

    return Message(message='Squad created successfully')

@router.get('/read-one', status_code=status.HTTP_200_OK, response_description='Read one squad with id', response_model=SquadRead)
def read_one_squad_with_id(squad_id: int):
    squadDAO = SquadDAO()
    squad = squadDAO.read_one_with_id(squad_id)
    
    if not squad:
        raise HTTPException(status_code=404, detail='Squad not found')
    
     # Convert the tuple to a dictionary
    squad = dict(zip(['id', 'name'], squad))

    return squad

@router.get('/read-all', status_code=status.HTTP_200_OK, response_description='Read all squads', response_model=list[SquadRead])
def read_all_squads():
    squadDAO = SquadDAO()
    squads = squadDAO.read_all()
    
    if not squads:
        raise HTTPException(status_code=404, detail='No squads found')
    
    # Convert the list of tuples to a list of dictionaries
    squads = [dict(zip(['id', 'name'], squad)) for squad in squads]

    return squads

@router.get('/read-spent-hours', status_code=status.HTTP_200_OK, response_description='Read spent hours from employees in a squad', response_model=list[EmployeeHours])
def get_spent_hours_from_squad(
    squad_id: int,
    start_date: datetime = Query(..., description="Data de início"),
    end_date: datetime = Query(..., description="Data de término")
):
    squadDAO = SquadDAO()
    squad = squadDAO.read_one_with_id(squad_id)
    
    if not squad:
        raise HTTPException(status_code=404, detail='Squad not found')
        
    squadDAO = SquadDAO()
    spent_hours = squadDAO.read_spent_hours_from_squad(squad_id, start_date, end_date) 
    
    if not spent_hours:
        raise HTTPException(status_code=404, detail='No spent hours found')
    
    response = [
        EmployeeHours(employeeId=row[0], employeeName = row[1], spentHours = row[2])
        for row in spent_hours
    ]

    return response

@router.get('/read-total-spent-hours', status_code=status.HTTP_200_OK, response_description='Read total spent hours from employees in a squad', response_model=TotalHours)
def get_total_spent_hours_from_squad(
    squad_id: int,
    start_date: datetime = Query(..., description="Data de início"),
    end_date: datetime = Query(..., description="Data de término")
):
    squadDAO = SquadDAO()
    squad = squadDAO.read_one_with_id(squad_id)
    
    if not squad:
        raise HTTPException(status_code=404, detail='Squad not found')
        
    squadDAO = SquadDAO()
    spent_hours = squadDAO.read_total_spent_hours_from_squad(squad_id, start_date, end_date) 
    
    if not spent_hours:
        raise HTTPException(status_code=404, detail='No spent hours found')
    
    
    response = TotalHours(squadId= squad_id, squadName= squad[1],  totalHours= spent_hours[0][0])
    
    return response

@router.get('/read-average-spent-hours', status_code=status.HTTP_200_OK,  response_description='Read average spent hours from employees in a squad', response_model=AverageHours)
def get_average_spent_hours_from_squad(
    squad_id: int,
    start_date: datetime = Query(..., description="Data de início"),
    end_date: datetime = Query(..., description="Data de término")
):
    squadDAO = SquadDAO()
    squad = squadDAO.read_one_with_id(squad_id)
    
    if not squad:
        raise HTTPException(status_code=404, detail='Squad not found')
        
    squadDAO = SquadDAO()
    spent_hours = squadDAO.read_average_spent_hours_from_squad(squad_id, start_date, end_date)
    
    if spent_hours is None:
        raise HTTPException(status_code=404, detail="No reports found for the specified squad and period")

    average = spent_hours[0][0]/spent_hours[0][1]

    response = AverageHours(
        squadId=squad_id,
        averageHoursPerDay=round(average, 2)
    )
    return response