from datetime import datetime
from fastapi import APIRouter, Query, status, Body, HTTPException
from typing import List

from src.utils import Message
from src.models.report_model import ReportBase, ReportRead, ReportsFromSquad
from src.database.repositories.report_repository import ReportDAO
from src.database.repositories.employee_repository import EmployeeDAO

router = APIRouter()

@router.post('/create', status_code=status.HTTP_201_CREATED, response_description='Create new report', response_model=Message)
def create_report(new_report: ReportBase = Body(...)):
    reportDAO = ReportDAO()
    employeeDAO = EmployeeDAO()

    employee = employeeDAO.read_one_with_id(new_report.employee_id)
    if not employee: # If employee doesn't exist, return a 409 status code
        raise HTTPException(status_code=409, detail='Employee not found')
    
    created_status = reportDAO.create(new_report)
    if not created_status:
        raise HTTPException(status_code=500, detail='Internal server error')

    return Message(message='Report created successfully')

@router.get('/read-all-from-employee', status_code=status.HTTP_200_OK, response_description='Read all reports from employee', response_model=List[ReportRead])
def read_all_reports_from_employee(employee_id: int):
    reportDAO = ReportDAO()

    reports = reportDAO.read_all_from_employee(employee_id)
    if not reports:
        raise HTTPException(status_code=404, detail='Reports not found')

    # Convert the list of tuples to a list of dictionaries
    reports = [dict(zip(['id', 'description', 'employeeId', 'spentHours', 'createdAt'], report)) for report in reports]
    return reports

@router.get('/read-all-reports-from-squad', status_code=status.HTTP_200_OK, response_description='Read all reports from employee', response_model=List[ReportsFromSquad])
def read_all_reports_from_squad(squad_id: int,  start_date: datetime = Query(..., description="Data de início"),
    end_date: datetime = Query(..., description="Data de término")):
    reportDAO = ReportDAO()

    reports = reportDAO.read_all_reports_from_squad(squad_id, start_date, end_date)
    print(reports)
    if not reports:
        raise HTTPException(status_code=404, detail='Reports not found')

    # Convert the list of tuples to a list of dictionaries
    reports = [dict(zip(['member', 'description', 'spentHours', 'createdAt'], report)) for report in reports]
    return reports

