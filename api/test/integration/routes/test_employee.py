from fastapi.testclient import TestClient
from unittest.mock import patch
import test.integration.mocks.mock_employee as mock

@patch('src.app.routes.employee.EmployeeDAO.read_all')
def test_read_all_employees(mock_read_all, client: TestClient):
    mock_read_all.return_value = [(1, "Matheus", 8, 1), (2, "Ana", 8, 1), (3, "Carlos", 6, 2)]
    
    response = client.get('/employee/read-all')
    
    expected_response = mock.valid_all_employees()
    assert response.status_code == 200
    assert response.json() == expected_response

@patch('src.app.routes.employee.EmployeeDAO.read_all')
def test_read_all_employees_not_found(mock_read_all, client: TestClient):
    mock_read_all.return_value = []
    
    response = client.get('/employee/read-all')
    
    assert response.status_code == 404
    assert response.json()['detail'] == 'No employees found'

@patch('src.app.routes.employee.EmployeeDAO.read_one_with_id')
def test_read_one_employee(mock_read_one_with_id, client: TestClient):
    mock_read_one_with_id.return_value = (1, "Matheus", 8, 1)
    
    valid_employee_id = 1
    response = client.get(f'/employee/read?employee_id={valid_employee_id}')
    
    expected_response = mock.valid_employee()
    assert response.status_code == 200
    assert response.json() == expected_response 

@patch('src.app.routes.employee.EmployeeDAO.read_one_with_id')
def test_read_one_employee_not_found(mock_read_one_with_id, client: TestClient):
    mock_read_one_with_id.return_value = None
    
    invalid_employee_id = 1
    response = client.get(f'/employee/read?employee_id={invalid_employee_id}')
    
    assert response.status_code == 404
    assert response.json()['detail'] == 'Employee not found'

@patch('src.app.routes.employee.SquadDAO.read_one_with_id')
@patch('src.app.routes.employee.EmployeeDAO.read_one_with_name')
@patch('src.app.routes.employee.EmployeeDAO.create')
def test_create_employee(mock_create, mock_read_one_with_name, mock_read_one_with_id, client: TestClient):
    mock_read_one_with_id.return_value = (1, "back-end")
    mock_read_one_with_name.return_value = None
    mock_create.return_value = True
    
    body = mock.valid_create_employee()
    response = client.post(f'/employee/create', json=body)
    
    assert response.status_code == 201
    assert response.json()['message'] == 'Employee created successfully'

@patch('src.app.routes.employee.SquadDAO.read_one_with_id')
@patch('src.app.routes.employee.EmployeeDAO.read_one_with_name')
@patch('src.app.routes.employee.EmployeeDAO.create')
def test_create_employee_no_squad_found(mock_create, mock_read_one_with_name, mock_read_one_with_id, client: TestClient):
    mock_read_one_with_id.return_value = None
    mock_read_one_with_name.return_value = None
    mock_create.return_value = True
    
    body = mock.valid_create_employee()
    response = client.post(f'/employee/create', json=body)
    
    assert response.status_code == 404
    assert response.json()['detail'] == 'Squad not found'
     
@patch('src.app.routes.employee.SquadDAO.read_one_with_id')
@patch('src.app.routes.employee.EmployeeDAO.read_one_with_name')
@patch('src.app.routes.employee.EmployeeDAO.create')
def test_create_employee_already_exist(mock_create, mock_read_one_with_name, mock_read_one_with_id, client: TestClient):
    mock_read_one_with_id.return_value = (1, "back-end")
    mock_read_one_with_name.return_value = (1, "Julia", 8, 1)
    mock_create.return_value = True
    
    body = mock.valid_create_employee()
    response = client.post(f'/employee/create', json=body)
    
    assert response.status_code == 409
    assert response.json()['detail'] == 'Employee with this name already exists'
     
