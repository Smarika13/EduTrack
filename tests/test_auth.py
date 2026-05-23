def test_register_success(client):
    response = client.post("/api/v1/register", json={
        "roll_no": "nce079bct036",
        "semester": 5,
        "dob": "2000-10-12",
        "name": "Pramisha",
        "email": "pramisha123@gmail.com",
        "phone": "9876543210",
        "faculty": "BCT",
        "password": "Pramisha@123#"})
    print(response.json())
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "pramisha123@gmail.com"
    assert "id" in data
    assert "hashed_password" not in data
    assert data["name"] == "Pramisha"
    assert data["faculty"] == "BCT"


def test_register_duplicate_email(client):
    response = client.post("/api/v1/register", json={
        "roll_no": "nce079bct036",
        "semester": 5,
        "dob": "2000-10-12",
        "name": "Pramisha",
        "email": "pramisha123@gmail.com",
        "phone": "9876543210",
        "faculty": "BCT",
        "password": "Pramisha@123#"})
    response = client.post("/api/v1/register", json={
        "roll_no": "nce079bct036",
        "semester": 5,
        "dob": "2000-10-12",
        "name": "Pramisha",
        "email": "pramisha123@gmail.com",
        "phone": "9876543210",
        "faculty": "BCT",
        "password": "Pramisha@123#"})
    print(response.json())
    assert response.status_code == 400
    assert response.json()["message"] == "Email already registered"


def test_register_invalid_data(client):
    response = client.post("/api/v1/register", json={})
    print(response.json())
    assert response.status_code == 422


def test_login_success(client):
    response = client.post("/api/v1/register", json={
        "roll_no": "nce079bct036",
        "semester": 5,
        "dob": "2000-10-12",
        "name": "Pramisha",
        "email": "pramisha123@gmail.com",
        "phone": "9876543210",
        "faculty": "BCT",
        "password": "Pramisha@123#"})
    response = client.post("/api/v1/login", json={
        "email": "pramisha123@gmail.com",
        "password": "Pramisha@123#"})
    data = response.json()
    assert response.status_code == 200
    assert "access_token" in data
    assert data["token_type"] == "bearer"
    assert "refresh_token" in data


def test_login_invalid_credentials(client):
    response = client.post("/api/v1/register", json={
        "roll_no": "nce079bct036",
        "semester": 5,
        "dob": "2000-10-12",
        "name": "Pramisha",
        "email": "pramisha123@gmail.com",
        "phone": "9876543210",
        "faculty": "BCT",
        "password": "Pramisha@123#"})
    response = client.post("/api/v1/login", json={
        "email": "pramisha123@gmail.com",
        "password": "pramisha@123#"})
    assert response.status_code == 401
