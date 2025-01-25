from fastapi.testclient import TestClient
from unittest.mock import patch
import test.integration.mocks.mock_squad as mock
import datetime

@patch('src.app.routes.squad.SquadDAO.read_one_with_name')
@patch('src.app.routes.squad.SquadDAO.create')
def test_create_squad(mock_create, mock_read_one_with_name, client: TestClient):
    mock_read_one_with_name.return_value = None
    mock_create.return_value = True
    
    body = mock.valid_create_squad()
    response = client.post(f'/squad/create', json=body)
    
    assert response.status_code == 201
    assert response.json()['message'] == 'Squad created successfully'

@patch('src.app.routes.squad.SquadDAO.read_one_with_name')
@patch('src.app.routes.squad.SquadDAO.create')
def test_create_squad_faild_invalid_name(mock_create, mock_read_one_with_name, client: TestClient):
    mock_read_one_with_name.return_value = None
    mock_create.return_value = True
    
    body = mock.invalid_create_squad()
    response = client.post(f'/squad/create', json=body)
    
    assert response.status_code == 422
    assert response.json()['detail'] == 'Name cannot be an empty string'

@patch('src.app.routes.squad.SquadDAO.read_one_with_name')
def test_create_squad_faild_name_already_exist(mock_read_one_with_name, client: TestClient):
    mock_read_one_with_name.return_value = (1, "front-end")
    
    body = mock.squad()
    response = client.post(f'/squad/create', json=body)
    
    assert response.status_code == 409
    assert response.json()['detail'] == 'Squad with this name already exists'
    
@patch('src.app.routes.squad.SquadDAO.read_one_with_id')
def test_read_one(mock_read_one_with_id, client: TestClient):
    mock_read_one_with_id.return_value = (1, "back-end")
    
    squad_id = 1
    response = client.get(f'/squad/read-one?squad_id={squad_id}')
    
    expected_response = mock.valid_read_squad()
    assert response.status_code == 200
    assert response.json() == expected_response

@patch('src.app.routes.squad.SquadDAO.read_one_with_id')
def test_read_one_squad_not_found(mock_read_one_with_id, client: TestClient):
    mock_read_one_with_id.return_value = None
    
    squad_id = 4
    response = client.get(f'/squad/read-one?squad_id={squad_id}')
    
    assert response.status_code == 404
    assert response.json()['detail'] == "Squad not found"

@patch('src.app.routes.squad.SquadDAO.read_all')
def test_read_all(mock_read_all, client: TestClient):
    mock_read_all.return_value = [(1, "back-end"), (2, "front-end")]
    
    response = client.get(f'/squad/read-all')
    
    expected_response = mock.read_all_squads()
    assert response.status_code == 200
    assert response.json() == expected_response

@patch('src.app.routes.squad.SquadDAO.read_all')
def test_read_all_faild_squads_not_found(mock_read_all, client: TestClient):
    mock_read_all.return_value = None
    
    response = client.get(f'/squad/read-all')
    
    assert response.status_code == 404
    assert response.json()['detail'] == "No squads found"
    
@patch('src.app.routes.squad.SquadDAO.read_spent_hours_from_squad')
@patch('src.app.routes.squad.SquadDAO.read_one_with_id')
def test_read_spent_hours(mock_read_one_with_id, mock_read_spent_hours_from_squad, client: TestClient):
    mock_read_one_with_id.return_value = (1, "back-end")
    mock_read_spent_hours_from_squad.return_value = [(1, "Matheus", 16), (2, "Ana", 8)]
    
    valid_squad_id = 1
    valid_start_date = "2025-01-20T21:06:14.997Z"
    valid_end_date = "2025-01-30T21:06:14.997Z"
    response = client.get(f'/squad/read-spent-hours?squad_id={valid_squad_id}&start_date={valid_start_date}&end_date={valid_end_date}')
    
    expected_response = mock.valid_read_spent_hours_response()
    assert response.status_code == 200
    assert response.json() == expected_response

@patch('src.app.routes.squad.SquadDAO.read_one_with_id')
def test_read_spent_hours_faild_squad_not_found(mock_read_one_with_id, client: TestClient):
    mock_read_one_with_id.return_value = None
    
    valid_squad_id = 4
    valid_start_date = "2025-01-20T21:06:14.997Z"
    valid_end_date = "2025-01-30T21:06:14.997Z"
    response = client.get(f'/squad/read-spent-hours?squad_id={valid_squad_id}&start_date={valid_start_date}&end_date={valid_end_date}')
    
    assert response.status_code == 404
    assert response.json()['detail'] == "Squad not found"

@patch('src.app.routes.squad.SquadDAO.read_spent_hours_from_squad')
@patch('src.app.routes.squad.SquadDAO.read_one_with_id')
def test_read_spent_hours_faild_no_spent_hours_found(mock_read_one_with_id, mock_read_spent_hours_from_squad, client: TestClient):
    mock_read_one_with_id.return_value = (1, "back-end")
    mock_read_spent_hours_from_squad.return_value = None
    
    valid_squad_id = 1
    valid_start_date = "2025-01-20T21:06:14.997Z"
    valid_end_date = "2025-01-30T21:06:14.997Z"
    response = client.get(f'/squad/read-spent-hours?squad_id={valid_squad_id}&start_date={valid_start_date}&end_date={valid_end_date}')
    
    assert response.status_code == 404
    assert response.json()['detail'] == "No spent hours found"

@patch('src.app.routes.squad.SquadDAO.read_total_spent_hours_from_squad')
@patch('src.app.routes.squad.SquadDAO.read_one_with_id')
def test_read_total_spent_hours(mock_read_one_with_id, mock_read_total_spent_hours_from_squad, client: TestClient):
    mock_read_one_with_id.return_value = (1, "back-end")
    mock_read_total_spent_hours_from_squad.return_value = [(24, 1)]
    
    valid_squad_id = 1
    valid_start_date = "2025-01-20T21:06:14.997Z"
    valid_end_date = "2025-01-30T21:06:14.997Z"
    response = client.get(f'/squad/read-total-spent-hours?squad_id={valid_squad_id}&start_date={valid_start_date}&end_date={valid_end_date}')
    
    expected_response = mock.valid_read_total_spent_hours_response()
    assert response.status_code == 200
    assert response.json() == expected_response

@patch('src.app.routes.squad.SquadDAO.read_one_with_id')
def test_read_total_spent_hours_faild_no_squad_found(mock_read_one_with_id, client: TestClient):
    mock_read_one_with_id.return_value = None
    
    valid_squad_id = 10
    valid_start_date = "2025-01-20T21:06:14.997Z"
    valid_end_date = "2025-01-30T21:06:14.997Z"
    response = client.get(f'/squad/read-total-spent-hours?squad_id={valid_squad_id}&start_date={valid_start_date}&end_date={valid_end_date}')
    
    assert response.status_code == 404
    assert response.json()['detail'] == "Squad not found"

@patch('src.app.routes.squad.SquadDAO.read_total_spent_hours_from_squad')
@patch('src.app.routes.squad.SquadDAO.read_one_with_id')
def test_read_total_spent_hours_faild_no_squad_found(mock_read_one_with_id, mock_read_total_spent_hours_from_squad, client: TestClient):
    mock_read_one_with_id.return_value = (2, "front-end")
    mock_read_total_spent_hours_from_squad.return_value = None
    
    valid_squad_id = 2
    valid_start_date = "2025-01-20T21:06:14.997Z"
    valid_end_date = "2025-01-30T21:06:14.997Z"
    response = client.get(f'/squad/read-total-spent-hours?squad_id={valid_squad_id}&start_date={valid_start_date}&end_date={valid_end_date}')
    
    assert response.status_code == 404
    assert response.json()['detail'] == "No spent hours found"
    
@patch('src.app.routes.squad.SquadDAO.read_average_spent_hours_from_squad')
@patch('src.app.routes.squad.SquadDAO.read_one_with_id')
def test_read_average_spent_hours(mock_read_one_with_id, mock_read_average_spent_hours_from_squad, client: TestClient):
    mock_read_one_with_id.return_value = (1, "back-end")
    mock_read_average_spent_hours_from_squad.return_value = [(24, 10)]
    
    valid_squad_id = 1
    valid_start_date = "2025-01-21T21:06:14.997Z"
    valid_end_date = "2025-01-30T21:06:14.997Z"
    response = client.get(f'/squad/read-average-spent-hours?squad_id={valid_squad_id}&start_date={valid_start_date}&end_date={valid_end_date}')
    
    expected_response = mock.valid_read_average_spent_hours_response()
    assert response.status_code == 200
    assert response.json() == expected_response

@patch('src.app.routes.squad.SquadDAO.read_one_with_id')
def test_read_average_spent_hours_faild_squad_not_found(mock_read_one_with_id, client: TestClient):
    mock_read_one_with_id.return_value = None
    
    valid_squad_id = 1
    valid_start_date = "2025-01-21T21:06:14.997Z"
    valid_end_date = "2025-01-30T21:06:14.997Z"
    response = client.get(f'/squad/read-average-spent-hours?squad_id={valid_squad_id}&start_date={valid_start_date}&end_date={valid_end_date}')
    
    assert response.status_code == 404
    assert response.json()['detail'] == "Squad not found"
    
@patch('src.app.routes.squad.SquadDAO.read_average_spent_hours_from_squad')
@patch('src.app.routes.squad.SquadDAO.read_one_with_id')
def test_read_average_spent_hours_faild_no_reports_found(mock_read_one_with_id, mock_read_average_spent_hours_from_squad, client: TestClient):
    mock_read_one_with_id.return_value = (2, "back-end")
    mock_read_average_spent_hours_from_squad.return_value = None
    
    valid_squad_id = 2
    valid_start_date = "2025-01-21T21:06:14.997Z"
    valid_end_date = "2025-01-30T21:06:14.997Z"
    response = client.get(f'/squad/read-average-spent-hours?squad_id={valid_squad_id}&start_date={valid_start_date}&end_date={valid_end_date}')
    
    assert response.status_code == 404
    assert response.json()['detail'] == "No reports found for the specified squad and period"