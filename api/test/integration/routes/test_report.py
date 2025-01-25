from fastapi.testclient import TestClient
from unittest.mock import patch
import test.integration.mocks.mock_report as mock
import datetime

@patch('src.app.routes.report.EmployeeDAO.read_one_with_id')
@patch('src.app.routes.report.ReportDAO.create')
def test_create_report(mock_create, mock_read_one_with_id, client: TestClient):
    mock_read_one_with_id.return_value = (1, "Julia", 8, 1)
    mock_create.return_value = True
    
    body = mock.valid_create_report()
    response = client.post(f'/report/create', json=body)
    
    assert response.status_code == 201
    assert response.json()['message'] == 'Report created successfully'

@patch('src.app.routes.report.EmployeeDAO.read_one_with_id')
@patch('src.app.routes.report.ReportDAO.create')
def test_create_report_fail_employee_not_found(mock_create, mock_read_one_with_id, client: TestClient):
    mock_read_one_with_id.return_value = None
    mock_create.return_value = True
    
    body = mock.valid_create_report()
    response = client.post(f'/report/create', json=body)
    
    assert response.status_code == 409
    assert response.json()['detail'] == 'Employee not found'

@patch('src.app.routes.report.ReportDAO.read_all_from_employee')
def test_read_all_from_employee(mock_read_all_from_employee, client: TestClient):
    mock_read_all_from_employee.return_value = [(1, "Realizando back-end", 1, 6, datetime.datetime(2025, 1, 25, 13, 17, 11, 489292)), (2, "Refatorando API", 1, 8, datetime.datetime(2025, 1, 24, 10, 27, 10, 534334))]
    
    employee_id = 1
    response = client.get(f'/report/read-all-from-employee?employee_id={employee_id}')
    
    expected_response = mock.valid_read_all_reports_from_employee()
    assert response.status_code == 200
    assert response.json() == expected_response

@patch('src.app.routes.report.ReportDAO.read_all_from_employee')
def test_read_all_from_employee_fail_not_found(mock_read_all_from_employee, client: TestClient):
    mock_read_all_from_employee.return_value = None
    
    employee_id = 4
    response = client.get(f'/report/read-all-from-employee?employee_id={employee_id}')
    
    assert response.status_code == 404
    assert response.json()['detail'] == "Reports not found"
    
@patch('src.app.routes.report.ReportDAO.read_all_reports_from_squad')
def test_read_all_reports_from_squad(mock_read_all_reports_from_squad, client: TestClient):
    mock_read_all_reports_from_squad.return_value = [("Matheus", "Realizando back-end", 4, datetime.datetime(2025, 1, 25, 13, 17, 11, 489292)), ("Ana", "Refatorando API", 6, datetime.datetime(2025, 1, 23, 13, 17, 10, 534334))]
    
    valid_squad_id = 1
    valid_start_date = "2025-01-20T21:06:14.997Z"
    valid_end_date = "2025-01-30T21:06:14.997Z"
    response = client.get(f'/report/read-all-reports-from-squad?squad_id={valid_squad_id}&start_date={valid_start_date}&end_date={valid_end_date}')
    
    expected_response = mock.valid_read_all_reports_from_squad()
    assert response.status_code == 200
    assert response.json() == expected_response

@patch('src.app.routes.report.ReportDAO.read_all_reports_from_squad')
def test_read_all_reports_from_squad_fail(mock_read_all_reports_from_squad, client: TestClient):
    mock_read_all_reports_from_squad.return_value = None
    
    valid_squad_id = 1
    valid_start_date = "2025-01-20T21:06:14.997Z"
    valid_end_date = "2025-01-30T21:06:14.997Z"
    response = client.get(f'/report/read-all-reports-from-squad?squad_id={valid_squad_id}&start_date={valid_start_date}&end_date={valid_end_date}')
    
    assert response.status_code == 404
    assert response.json()['detail'] == "Reports not found"
    
